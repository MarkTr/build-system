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
from conary import cvc
from rmake.cmdline import main as rmk

versionString="%prog 0.1"   
gitPack = ['midori', 'ristretto']
cwd = os.getcwd()
cpk = conarypk.ConaryPk()
ilps = {'xd':'xfce.rpath.org@xfce:devel','fl2':'foresight.rpath.org@fl:2-devel'}
codirs = {'xd':'~/conary/src/xfce-devel/','fl2':'~/conary/src/fl2-devel/'}

pkglist = [
    'gtk-xfce-engine',
    'libexo',
    'libxfce4util',
    'libxfce4menu',
    'libxfcegui4',
    'xfce-utils',
    'xfconf',
    'thunar',
    'xfce4-dev-tools',
    'xfce4-panel',
    'xfce4-session',
    'xfce4-settings',
    'xfdesktop,xarchiver',
    'xfce4-mixer,orage',
    'xfwm4,xfwm4-themes',
    'xfce4-appfinder',
    'xfprint',
    'libxfce4ui',
    'xfburn',
    'xfce4-places-plugin',
    'xfce4-battery-plugin',
    'xfce4-cddrive-plugin',
    'thunar-volman',
    'xfce4-power-manager',
    'gigolo',
    'parole'
]

def load_pkglist():
    pass

def wipe_out(dir):
    dir = os.path.expanduser(dir)
    print 'delete ',dir
    sp.check_call(['rm','-rf',dir])
    
def chdir(dir):
    dir = os.path.expanduser(dir)
    print 'change directory:',dir
    os.chdir(dir)

def needsupdate_git(project, gitrepo):
    wipe_out('~/git/' + project)
    curgit = cpk.request_query(project, ilp)[0][1].trailingRevision().getVersion()
    #curgit.getSourceVersion()
    print 'latest version of ' + project + ' in conary is: ' + curgit
    chdir('~/git/')
    sp.check_call(['git-clone', '-q', '--depth', '1', '-n', gitrepo, project])
    chdir('~/git/' + project)        
    newgit =    sp.Popen(['git', 'rev-parse', '--short', 'HEAD'],
            stdout=sp.PIPE, stderr=sp.STDOUT).stdout.read().strip()
    print 'latest commit of ' + project + ' in git is: ' + newgit
    chdir(cwd)
    wipe_out('~/git/' + project)
    return (newgit != curgit)

def needsbuild(project):
    srev = cpk.request_query(project +':source', ilp)[0][1].trailingRevision()
    brev = cpk.request_query(project, ilp)[0][1].trailingRevision()
    print srev,srev.buildCount,srev.sourceCount, brev,brev.buildCount,brev.sourceCount
    return (srev.getVersion() != brev.getVersion() or
            srev.sourceCount != brev.sourceCount)

def refresh(project):
    print 'refresh: ' + project
    wipe_out(codir + project)
    chdir(codir)
    cvc.main(['refresh-xfce.py','co',project + '=' + ilp])
    chdir(codir + project)
    cvc.main(['refresh-xfce.py','refresh'])
    cvc.main(['refresh-xfce.py','ci', "-m'sync with upstream'"])
    chdir(cwd)
    
def update():
    if needsupdate_git(project, gitrepo):
        refresh(project)
    
    
def build():
    if needsbuild(project):
        print ('build')
    rmk.main(['refresh-xfce.py', 'build', project + '{x86}', '--commit', '--context=fl:2-devel'])
    
parser = OptionParser(usage ="usage: %prog [options] action\n"
                      "\nActions:\n"
                      "  update\t\tUpdate source\n"
                      "  build\t\t\tbuild source",
                      version=versionString)
parser.add_option("-r", "--repo",
                  help='Conary Repository:'
                       'xd - xfce.rpath.org@xfce:devel '
                       'fl2 - foresight.rpath.org@fl:2-devel '
                       '[default: %default]', default="xd")

(options, args) = parser.parse_args()
print (options)
print (args)
if len(args) !=1:
    parser.error("incorrect number of arguments")

ilp = ilps[options.repo]
codir = codirs[options.repo]
project = 'whaawmp'
if (args[0] == 'update'):
    gitrepo = 'http://git.gitorious.org/whaawmp/mainline.git'
    update()
elif (args[0] == 'build'):
    build()
elif (args[0] == 'all'):
    update()
    build()
else:
    parser.error("argument not allowed")
