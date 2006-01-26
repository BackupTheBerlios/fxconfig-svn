#! /usr/bin/python
#
# system-config-sudoers.py (c) 2005 Tejas Dinkar <tejasdinkar AT gmail DOT com>
#
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; version 2 of the License.
#
# This is a Part of a program that has not been named yet, developed by the
# team of Fedora Unity Developers: http://www.fedoraunity.org
#

import gtk
import gtk.glade

from fxconfig import sudoers

glade_file = 'system-config-sudoers/system-config-sudoers.glade'

class system_config_sudoers:

	def destroy(*args):
		'''Die you **** *******'''
		gtk.main_quit()

	def refresh_admins(self):
		'''This Refreshes The Window In the 'View Admins' Window'''
		admins_list = sudoers.users_in_wheel()
		string = "\n".join(admins_list)
		self.buffer.set_text(string)

	def toggle_enabled(self,*args):
		'''Is Called when the Enabled Box is Toggled'''
		self.write_sudoers()
		self.hide_passbox_if_needed()

	def toggle_password(self,*args):
		'''Is Called when the Password Box is Toggled'''
		self.write_sudoers()

	def write_sudoers(self):
		'''This Writes to the Sudoers File'''
		enabled = self.checkbox_enabled.get_active()
		password = self.checkbox_password.get_active()
		sudoers.write_sudoers(enabled,password)

	def hide_passbox_if_needed(self):
		'''This Hides The Password Box if needed'''
		if not self.checkbox_enabled.get_active():
			self.checkbox_password.hide()
		else:
			self.checkbox_password.show()

	def add_admin(self,*args):
		'''Adds an Admin to the Group Wheel'''
		name = self.admin_name.get_text()
		if not name:
			return
		result = sudoers.add_to_wheel(name)
		if result == 1:
			message("%s is already in the wheel group"  % name)
		elif result == 2:
			message("I'm met many people in my life, but %s is not one of them" % name)

		self.refresh_admins()

	def del_admin(self,*args):
		'''Removes an Admin from the Group Wheel'''
		name = self.admin_name.get_text()
		if not name:
			return
		result = sudoers.remove_from_wheel(name)
		if result == 1:
			message("%s is not in the wheel group"  % name)
		elif result == 2:
			message("I'm met many people in my life, but %s is not one of them" % name)
		self.refresh_admins()

	def show_about(self, *args):
		'''Show The About Box'''
		self.about.show_all()

	def __init__(self):
		self.xml = gtk.glade.XML(glade_file)

		# Connect all the Signals
		self.xml.signal_autoconnect({
			'on_delete_event': self.destroy,
			'on_check_enabled_toggled': self.toggle_enabled,
			'on_check_password_toggled': self.toggle_password,
			'on_button_add_clicked': self.add_admin,
			'on_button_del_clicked': self.del_admin,
			'show_about': self.show_about
		})

		self.about = self.xml.get_widget('aboutdialog')
		self.about.hide_all()

		self.buffer = self.xml.get_widget('admins_list').get_buffer()
		self.checkbox_enabled = self.xml.get_widget('check_enabled')
		self.checkbox_password = self.xml.get_widget('check_password')

		# Get the current state of sudo, and modify boxes
		current_state = sudoers.get_current_state()
		self.checkbox_enabled.set_active(current_state['enabled'])
		self.checkbox_password.set_active(current_state['pass_required'])

		self.admin_name = self.xml.get_widget('admin_name')
		self.refresh_admins()

	def main(self):
		gtk.main()

def message(string):
	'''This Bugs you with a Message'''
	dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, string)
        dlg.set_markup(string)
        dlg.set_position(gtk.WIN_POS_CENTER)
        dlg.set_modal(True)
        dlg.run()
        dlg.destroy()


if __name__ == '__main__':
	obj = system_config_sudoers()
	obj.main()
