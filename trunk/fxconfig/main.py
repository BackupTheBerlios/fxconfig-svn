#!/usr/bin/python

# This file is Temporary
# http://www.fedoraunity.org

import gtk
import os
import gtk.glade

def die(*args):
	'''Kills this Program'''
	gtk.main_quit()
	return False

print "You have reached FXConfig - Fedora eXtended Configurator, by the Fedora Unity Project. http://www.fedoraunity.org"
print "We are still in testing and devel phase"
print

gladepath = "fxconfig.glade"
xml = gtk.glade.XML(gladepath, domain='fxconfig')

xml.signal_autoconnect({
	'delete_event': die
})

xml.get_widget("window-fxconfig").show_all()

gtk.main()
