#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2009 Mark Trompell <mark@foresightlinux.org>
#
# Licensed under the GNU General Public License Version 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from optparse import OptionParser
import subprocess as sp
import os
import conarypk

versionString="%prog 0.1"	
gitPack = ['midori', 'ristretto']
cwd = os.getcwd()
cpk = conarypk.ConaryPk()
ilp = 'foresight.rpath.org@fl:2-devel'

def latest_git(project, gitrepo):
	curgit = cpk.request_query(project, ilp)[0][1].trailingRevision().getVersion()
	#curgit.getSourceVersion()
	print curgit
	os.chdir(os.path.expanduser('~/git/'))
	sp.check_call(['git-clone', '-q', '--depth', '1', '-n', gitrepo, project])
	os.chdir(os.path.expanduser('~/git/') + project)		
	newgit = 	sp.Popen(['git', 'rev-parse', '--short', 'HEAD'],
	        stdout=sp.PIPE, stderr=sp.STDOUT).stdout.read().strip()
	print newgit
	os.chdir(cwd)
	
	
def update(scm):
	latest_git(project, gitrepo)
	print (scm)
	
def build():
	print ('build')
	
parser = OptionParser(usage ="usage: %prog [options] action\n"
                      "\nActions:\n"
					  "  update\t\tUpdate source\n"
					  "  build\t\t\tbuild source",
					  version=versionString)
parser.add_option("-s", "--scm",
                  help="Source Code Management: git, svn or all"
				  " [default: %default]", default="all")

(options, args) = parser.parse_args()
print (options)
print (args)
if len(args) !=1:
	parser.error("incorrect number of arguments")

if (args[0] == 'update'):
	project = 'whaawmp'
	gitrepo = 'http://git.gitorious.org/whaawmp/mainline.git'
	update(options.scm)
elif (args[0] == 'build'):
	build()
elif (args[0] == 'all'):
	update(options.scm)
	build()
else:
	parser.error("argument not allowed")
