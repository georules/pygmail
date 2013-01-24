#!/usr/bin/env python
import sys,time,threading
from PyQt4.QtCore import QObject, QThread, pyqtSignal,QTimer
from PyQt4.QtGui import QApplication, QSystemTrayIcon, QMenu, QIcon, QStyle
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
	#def __init__(self, parent=None):
	#	QObject.__init__(self)
	#	self.update()
	#	self.timer = QTimer(self)
	#	self.timer.setInterval(waittime)
	#	self.timer.timeout.connect(self.update)
	#def start(self):
	#	self.timer.start()
	#def stop(self):
	#	self.timer.stop()
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
		menu = QMenu(parent)
		menu.addAction("Update",lambda:forceupdate())
		menu.addAction("Exit",lambda:close())
		self.setContextMenu(menu)
	def update(self):
		global data
		flag = False
		for key in data:
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
#threading.Thread(target=monitor.start).start()

sys.exit(app.exec_())
