#! /usr/bin/python
#
# mp3_things.py (c) 2005 Tejas Dinkar <tejasdinkar AT gmail DOT com>
#
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; version 2 of the License.
#
# This is a Part of a program that has not been named yet, developed by the
# team of Fedora Unity Developers: http://www.fedoraunity.org
#
# MUCH Faster way to query the RPM database given by: Panu Matilainen
#                         <pmatilai@laiskiainen.org>
#

from common import program_is_installed

class ProgramThatNeedsMp3:
	'''This is an object. It has 4 Items:
	* program name 
	* name of plugin
	* installed (indicates if program is installed)
	* has_plugin (indicated if program's mp3 plugin is installed)
	
	it checks the RPM db for presence of program / plugin when created,
	unless you specifically ask it not to'''
	
	def __init__(self, name, plugin, check = True):
		self.name = name
		self.plugin = plugin
		
		# Set Default Values
		self.installed = False
		self.has_plugin = False
		
		# If required, check status in RPM DB for presence of program
		# and plugin
		if check:
			self.__check_if_in_rpm_db__()
	
	def __check_if_in_rpm_db__(self):
		'''This sets value of has_plugin and installed, to indicate which
		components of the program have been installed'''
		if program_is_installed(self.name):
			self.installed = True
			if program_is_installed(self.plugin):
				self.has_plugin = True


def list_of_all_mp3_apps():
	'''This Returns a List of all programs that can use mp3 support
	This Does NOT consider if it is installed on your machine or not
	You have to do that yourself by looking at obj.installed'''
	
	# Just making a Set of Variables, and I'll compile this into a list later
	xmms = ProgramThatNeedsMp3(name = "xmms", plugin = "xmms-mp3")
	
	k3b = ProgramThatNeedsMp3(name = "k3b", plugin = "k3b-mp3")
	
	gstreamer = ProgramThatNeedsMp3(name = "gstreamer", 
		plugin = "gstreamer-plugins-mp3")
	
	bmp = ProgramThatNeedsMp3(name = "bmp", plugin = "bmp-mp3")
	
	vdr = ProgramThatNeedsMp3(name = "vdr", plugin = "vdr-mp3")
	
	libtunepimp = ProgramThatNeedsMp3(name = "libtunepimp", 
		plugin = "libtunepimp-mp3")
	
	
	# This Next Part makes the list
	program_list = []
	for k,v in locals().items():
		if k is not "program_list":
			program_list.append(v)
	
	return program_list

def list_of_programs_if(installed, has_plugin, programs = None):
	'''This Returns a list of Objects of apps that are follow the conditions
	installed will be true or false, as will has_plugin. Passing a List of 
	Programs will Save VALUABLE time so you need not query the DB'''
	
	if programs == None:
		programs = list_of_all_mp3_apps()
	
	# Return_list holds the final list
	return_list = []
	
	# This Block checks if a program is installed AND the mp3 plugin is Not
	for i in programs:
		if i.installed == installed:
			if i.has_plugin == has_plugin:
				return_list.append(i)
	
	return return_list


# There are a Few Short Cuts to call list_of_programs_if()
# you can get them from dir(mp3_things)
# They are defined using lambda here
who_has_mp3_support = lambda programs = None: list_of_programs_if(True, True, programs)
who_needs_mp3_support = lambda programs = None: list_of_programs_if(True, False, programs)
programs_not_installed = lambda programs = None: list_of_programs_if(False, False, programs)
programs_installed = lambda programs = None: who_needs_mp3_support(programs) + who_has_mp3_support(programs)


# Every thing Below this is just for testing purposes
if __name__ == '__main__':
	programs = list_of_all_mp3_apps()
	
	print "This is a Way to test this module"
	print

	print "Here are A List of All Programs that Can Have mp3 support:"
	for i in programs:
		print "  %s\t\t%s" % (i.name,i.plugin)
	print
	
	print "\nThere is a List of Programs you have installed: "
	for i in programs_installed(programs):
		print "%s " % i.name,
	print
	
	print "\nThese Applications Have mp3 plugins installed: "
	for i in who_has_mp3_support(programs):
		print "%s " % i.name,
	print
	
	print "\nThese plugins need to be installed for YOUR programs to have mp3"
	for i in who_needs_mp3_support(programs):
		print "%s " % i.plugin,
	print
	
	print "\nFedora Unity!!! Bringing Unity to the Fedora Community through Quality content"
