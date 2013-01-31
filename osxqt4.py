#!/usr/bin/env python
import sys,time,threading
from PyQt4.QtCore import QObject, QThread, pyqtSignal,QTimer
from PyQt4.QtGui import QAction, QApplication, QSystemTrayIcon, QMenu, QIcon, QStyle
from readgmail import gmaildata

waittime = 5*60
data = {}

t_stop = threading.Event()

def close():
	t_stop.set()
	sys.exit(0)

def update(a1, stop_event):
	while(not stop_event.is_set()):
		print "update"
		data = gmaildata()
		stop_event.wait(10)

class GMailMonitor(QThread):
	change = pyqtSignal()
	def update(self):
		print "called"
		global data
		data = gmaildata()
		self.change.emit()
	def run(self):
		while(True):
			self.update()
			time.sleep(waittime)

#bad hax
def forceupdate():
	global monitor
	monitor.update()

class SystemTrayIcon(QSystemTrayIcon):
	def __init__(self,icons,parent=None):
		self.icons = icons
		QSystemTrayIcon.__init__(self,icons[0],parent)
		self.menu = QMenu(parent)
		self.menu.addAction("Update",lambda:forceupdate())
		self.menu.addAction("Exit",lambda:close())
		self.setContextMenu(self.menu)
		self.actions = []
	def update(self):
		global data
		flag = False
		for a in self.actions:
			self.menu.removeAction(a)
		for key in data:
			a = QAction(key+": " + str(data[key]), self.menu)
			self.actions.append(a)
			self.menu.addAction(a)
			x = data[key]
			if x > 0:
				flag = True
		if flag:
			self.setIcon(icons[1])
		else:
			self.setIcon(icons[0])

def hideMacDockIcon():
    import AppKit
    NSApplicationActivationPolicyRegular = 0
    NSApplicationActivationPolicyAccessory = 1
    NSApplicationActivationPolicyProhibited = 2
    AppKit.NSApp.setActivationPolicy_(NSApplicationActivationPolicyProhibited)

app = QApplication(sys.argv)
hideMacDockIcon()

style = app.style()
icon1 = QIcon(style.standardPixmap(QStyle.SP_DialogYesButton))
icon2 = QIcon(style.standardPixmap(QStyle.SP_DialogNoButton))
icons = [icon1,icon2]

monitor = GMailMonitor()
trayicon = SystemTrayIcon(icons)
monitor.change.connect(trayicon.update)
trayicon.show()
monitor.start()

sys.exit(app.exec_())
