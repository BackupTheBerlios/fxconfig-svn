#! /usr/bin/python
#
# common.py (c) 2005 Tejas Dinkar <tejasdinkar AT gmail DOT com>
#
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; version 2 of the License.
#
# This is a Part of a program FXConfig, developed by the
# team of Fedora Unity Developers: http://www.fedoraunity.org
#

def program_is_installed(name):
	'''This Checks RPM DB if a Program is Installed
	It only accepts one parameter, the name of the program
	The name should be an exact match, without version or arch
	ex: xmms... and duh!!! name is a string'''
	import rpm
	
	# Transaction Set is Equivalent to the RPM DataBase
	TransactionSet = rpm.ts()
	
	# This Next Line is Equivalent to rpm -qa
	# installed is of class MatchIterator
	installed = TransactionSet.dbMatch("name",name)
	
	# This next line cuts down installed to only those which match the regex
	# installed.pattern("name", rpm.RPMMIRE_DEFAULT, name)
	
	# This next block is an UGLY work around. Basically, if there is an element in
	# installed, it will return true, else it will return false
	for i in installed:
		return True
	return False