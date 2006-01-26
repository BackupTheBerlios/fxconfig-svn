#! /usr/bin/python
#
# repo_things.py (c) 2005 Tejas Dinkar <tejasdinkar AT gmail DOT com>
#
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; version 2 of the License.
#
# This is a Part of a program FXConfig, developed by the
# team of Fedora Unity Developers: http://www.fedoraunity.org
#
# Repo Locations Provided by the Following Fedora Users:
#    Livna - Bob Jensen
#

from common import program_is_installed

fxconfig_dir = '/var/cache/fxconfig'

def make_folder():
	'''This Ensures that the FXConfig Directory is Present
	Will be executed on importing'''
	import os
	try:
		os.listdir(fxconfig_dir)
	except OSError:
		os.mkdir(fxconfig_dir)

make_folder()

class DummyCallback:
	'''A Callback Draws reports on progress. This can be done later,
	and will probably be done in another file. Just remember to have these 
	same set of arguments. Thanks to Paul Nasrat for what these args are:
	  what -- callback type, 
	  amount -- bytes processed
	  total -- total bytes
          mydata -- package key (hdr, path)
	  wibble -- user data - unused here'''
	
	def callback(self, what, amount, total, mydata, wibble):
		import os, rpm
		if what == rpm.RPMCALLBACK_INST_OPEN_FILE:
			hdr, path = mydata
			fd = os.open(path, os.O_RDONLY)
			return fd

class repo:
	'''This Represents A repository. It contains the Following Items:
	* name
	* url - where the rpm of the repo config files is found
	* local_rpm - where the file should be downloaded locally
	* repo_file - where the .repo file is saved locally.
	* rpm_name - How the repo is saved in Database (ex: livna-release)
	* installed - If the Repo is installed'''
	
	def __init__(self, name, url = None, local_rpm = None, 
		rpm_name = None, repo_file = None, installed = False):
		
		self.fxconfig_dir = fxconfig_dir
		self.name = name
		self.url = url
		
		# This Next Block Gives a Default Value to local_rpm
		if url != None and local_rpm == None:
			self.local_rpm = self.fxconfig_dir + "/" + url.split("/")[-1]
		else:
			self.local_rpm = local_rpm
		
		if rpm_name == None:
			self.rpm_name = name + "-release"
		else:
			self.rpm_name = rpm_name
			
		if program_is_installed(self.rpm_name):
			self.installed = True
		else:
			self.installed = False
			
		self.repo_file = repo_file
	
	def download_rpm(self):
		'''This Downloads the rpm to be installed. This returns 1 in 
		case of a Failure, and 0 for success'''
		import urllib
		try:
			urllib.urlretrieve(self.url,self.local_rpm)
		except:
			return 1
		return 0
	
	def install_rpm(self, Callback = DummyCallback):
		'''This installs the Downloaded Local RPM. It returns 0 for
		sucess and 2 for failure'''
		try:
			import os, rpm
			TransactionSet = rpm.ts()
			
			# This Next Line turns off GPG key checks
			TransactionSet.setVSFlags(-1)
			
			# This next block gets the header from the rpm
			fdno = os.open(self.local_rpm, os.O_RDONLY)
			header = TransactionSet.hdrFromFdno(fdno)
			os.close(fdno)
			
			# Add install of file
			TransactionSet.addInstall(header,(header,self.local_rpm), "u")
			
			# Function cb.callback reports on progress
			cb = Callback()
			
			# Install rpm
			TransactionSet.run(cb.callback,"")
			
			# Set flag
			self.installed = True
			
		except:
			return 2
		
		return 0
	
	def erase_rpm(self, Callback = DummyCallback):
		'''This erases this RPM from the database. It returns 0 for
		success and 3 for failure'''
		try:
			import rpm
			TransactionSet = rpm.ts()
			TransactionSet.addErase(self.rpm_name)
			cb = Callback()
			TransactionSet.run(cb.callback,'')
			self.installed = False
		except:
			return 3
		
		# This next block just removes the backup if it is saved
		# this may or may not happen
		import os
		try:
			os.remove(self.repo_file + ".rpmsave")
		except:
			pass
		return 0
		
	def disable_repo(self):
		'''This Disables the Repo. You can't enable it again using
		this Function, however'''
		
		# Get the conf file in string
		file = open(self.repo_file)
		string = file.read()
		file.close()
		
		# replace
		str_list = string.split("\n")
		string = ""
		for i in str_list:
			if i.startswith("enabled"):
				string = string + "enabled=0\n"
			else:
				string = string + i + "\n"
		
		# write conf file back
		file = open(self.repo_file,'w')
		file.write(string)
		file.close()
		
		
	def install_repo(self, Callback = DummyCallback, disabled = True):
		'''This is What you should call to install a repo.
		Callback is a function to measure progress while installing
		This returns 0 in success and +ve for Failure'''
		if self.installed:
			if self.erase_rpm():
				return 3
		if self.download_rpm():
			return 1
		if self.install_rpm(Callback):
			return 2
		if disabled:
			self.disable_repo()
		return 0

def repo_dict():
	'''This returns a Dictionary of all repos. You use it as such:
	  dict["repo-name"], which is an object of class repo'''
	  
	livna = repo(	
			name = "livna",
			url = "http://rpm.livna.org/livna-release4.rpm",
			rpm_name = "livna-release",
			repo_file = "/etc/yum.repos.d/livna.repo"
		)
	
	freshrpms = repo(
			name = "freshrpms",
			url = "http://ftp.freshrpms.net/pub/freshrpms/fedora/linux/4/freshrpms-release/freshrpms-release-1.1-1.fc.noarch.rpm",
			rpm_name = "freshrpms-release",
			repo_file = "/etc/yum.repos.d/freshrpms.repo"
		)
			
	rpmforge = repo(
			name = "rpmforge",
			url = "http://ftp.belnet.be/packages/dries.ulyssis.org/fedora/fc4/i386/RPMS.dries/rpmforge-release-0.2-2.2.fc4.rf.i386.rpm",
			rpm_name = "rpmforge-release",
			repo_file = "/etc/yum.repos.d/rpmforge.repo"
		)
			
	return locals()

def repo_list():
	'''This Returns a list of repos, without the name. It is iterable :)'''
	li = []
	for k,v in repo_dict().items():
		li.append(v)
	return li
	

if __name__ == '__main__':
	import os, sys
	if os.getuid() != 0:
		print "I only know one user... and his name is root!"
		sys.exit(1)
	repos = repo_list()
	print "You can Either install the repo, erase it, or install it in disabled mode"
	print "Be Warned: It is NOT recommended to use this script to install your repos"
	print "This script should be ideally called from somewhere else"
	print "If you really must use this, install livna, and remove all others"
	print "Of course, there are 3 built in repos: base, updates-released and extras"
	for i in repos:
		print
		if i.installed:
			print "%s is already installed. Reinstalling will remove it" % i.name
		ans = raw_input("Install %s? [y/n/d/e] " % i.name)
		if 'y' in ans.lower():
			bug = i.install_repo(disabled = False)
		elif 'e' in ans.lower():
			bug = i.erase_rpm()
		elif 'd' in ans.lower():
			bug = i.install_repo(disabled = True)
		else:
			continue
		if bug:
				print "Bug %d found... Go Debug!" % bug
