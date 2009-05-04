#!/usr/bin/python
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

versionString="%prog 0.1"	
gitPack = ['midori', 'ristretto']
svnPack = ['gtk-xfce-engine', 'libexo,libxfce4util', 'libxfce4menu', 
           'libxfcegui4', 'xfce-utils', 'xfconf', 'thunar', 'xfce4-dev-tools', 
		   'xfce4-panel', 'xfce4-session', 'xfce4-settings', 'xfdesktop',
		   'xarchiver', 'xfce4-mixer', 'orage', 'xfwm4', 'xfwm4-themes', 
		   'xfce4-appfinder', 'xfprint',
		   ]
def update(scm):
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
	update(options.scm)
elif (args[0] == 'build'):
	build()
elif (args[0] == 'all'):
	update(options.scm)
	build()
else:
	parser.error("argument not allowed")
