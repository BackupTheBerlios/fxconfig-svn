#!/usr/bin/python
#
# sudoers.py (c) 2005 Tejas Dinkar <tejasdinkar AT gmail DOT com>
#
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; version 2 of the License.
#
# This is a Part of a program that has not been named yet, developed by the
# team of Fedora Unity Developers: http://www.fedoraunity.org
#

sudoers_file = '/etc/sudoers'
groups_file = '/etc/group'

sudoers_content = """
# sudoers file.
#
# This file MUST be edited with the 'visudo' command as root.
#
# See the sudoers man page for the details on how to write a sudoers file.
#

# Host alias specification

# User alias specification

# Cmnd alias specification

# Defaults specification

# Runas alias specification

# User privilege specification
root	ALL=(ALL) ALL

# Uncomment to allow people in group wheel to run all commands
# %wheel	ALL=(ALL)	ALL

# Same thing without a password
# %wheel	ALL=(ALL)	NOPASSWD: ALL

# Samples
# %users  ALL=/sbin/mount /cdrom,/sbin/umount /cdrom
# %users  localhost=/sbin/shutdown -h now
"""

chmod640 = 416
chmod440 = 288

def decide_string(enabled, password_required):
	'''This decides what string to write to sudoers. Don't call this manually'''

	string = sudoers_content	

	if enabled:
		if password_required:
			string = string.replace(
				"# %wheel	ALL=(ALL)	ALL",
				"%wheel	ALL=(ALL)	ALL"
				)
		else:
			string = string.replace(
				"# %wheel	ALL=(ALL)	NOPASSWD: ALL",
				"%wheel	ALL=(ALL)	NOPASSWD: ALL"
				)

	return string
			

def write_sudoers(enabled = True, password_required = False):
	'''Writes the Sudoers File... If you want this to allow users in wheel to use sudo, set enabled as true, and password does the obvious'''
	
	import os

	# next line gets content to write to sudoers
	string = decide_string(enabled, password_required)

	# sudoers file is read only, so we need to edit the perms
	os.chmod(sudoers_file,chmod640)

	# next block line writes it
	file = open(sudoers_file,'w')
	file.write(string)
	file.close()

	# next line reverts permissions
	os.chmod(sudoers_file, chmod440)

def add_to_wheel(user):
	'''This Adds a User to Wheel
	If a user already lives in wheel, he will not be added
	Returns 0 for normal exit, 
	1 if user is in wheel, 
	and 2 if user does not exist at all'''
	import os

	# This next block gets the current groups
	pipe = os.popen("groups %s" % user)
	string = pipe.read()
	pipe.close()
	if not string:
		return 2
	current_groups = string.split(":")[-1].strip().split()
	
	# Next line checks if a User is already in wheel
	if 'wheel' in current_groups:
		return 1
	else:
		groups = current_groups + ['wheel']
		os.system("/usr/sbin/usermod -G %s %s" %
			(",".join(groups), user) 
		)
	return 0

def remove_from_wheel(user):
	'''This Adds a User to Wheel
	If a user already lives in wheel, he will not be added
	Returns 0 for normal exit, 
	1 if user is not in wheel, 
	and 2 if user does not exist at all'''
	import os

	# This next block gets the current groups
	pipe = os.popen("groups %s" % user)
	string = pipe.read()
	pipe.close()
	if not string:
		return 2
	current_groups = string.split(":")[-1].strip().split()
	
	# Next line checks if a User is already in wheel
	if 'wheel' not in current_groups:
		return 1
	else:
		current_groups.remove('wheel')
		groups = current_groups
		os.system("/usr/sbin/usermod -G %s %s" %
			(",".join(groups), user) 
		)
	return 0

def users_in_wheel():
	'''This returns a List of All users in the Group Wheel'''
	file = open(groups_file,'r')
	for i in file:
		if i.startswith("wheel"):
			file.close()
			string = i.split(":")[-1].strip()
			break
	users = string.split(",")
	return users	

def get_current_state():
	'''This returns a dictionary with values, like 'enabled' and 'pass_requirerd' '''
	file = open(sudoers_file,'r')
	lines = file.readlines()
	file.close()

	values = {}

	if "%wheel	ALL=(ALL)	ALL\n" in lines:
		values['enabled'] = True
		values['pass_required'] = True
	elif "%wheel	ALL=(ALL)	NOPASSWD: ALL\n" in lines:
		values['enabled'] = True
		values['pass_required'] = False
	else:
		values['enabled'] = False
		values['pass_required'] = False

	return values

if __name__ == '__main__':

	ans = raw_input("Do you want to enable Sudo? ")
	if 'y' in ans.lower():
		enabled = True
	else:
		enabled = False

	if enabled:
		ans = raw_input("Do you want to ask for a Password on each use? ")
	if 'y' in ans.lower():
		password_required = True
	else:
		password_required = False

	write_sudoers(enabled, password_required)

	print "Sudoers Written"

	ans = raw_input("Who do You Want to add to wheel? Leave Blank for none: ")
	if ans:
		add_to_wheel(ans)
	else:
		print "Not editing groups"
