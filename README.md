pygmail
=======
I have multiple shared gmail accounts that I just want notification if there are unread messages.  I made this package to check these accounts and notify me if there are unread messages.  This is by no means user-friendly, well-organized, or ready for anyone to use.  If you're browsing, feel free to make suggestions.

Currently "working"
-------------------
*An OSX System Tray icon which changes if there are unread messages
*checkgmail.py scrapes gmail atom feed
*readgmail.py reads a configuration file "accounts"

Config file format
-----------
As many of the following as you want:

    [accountname]
    username = user_here
    password = pw_here


To-do
-----
* Organize modules
* Create notification system
* Notifications which tell you which account has unread messages
* Port to other operating systems
* UI for adding-removing accounts
* Anything that makes it cool, really.

Dependencies
------------
Just a few notes about modules that might not be default.
*checkgmail.py readmail method requires feedparser
*osxqt4.py requires pyqt4
*iconwx/iconwx2 are just copy-pasted demos of pythonwx I haven't tried yet

