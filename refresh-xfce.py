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
cwd = os.getcwd()
cpk = conarypk.ConaryPk()
gitrepo = 'http://git.xfce.org/'
ilps = {'xd':'xfce.rpath.org@xfce:devel','fl2':'foresight.rpath.org@fl:2-devel'}
codirs = {'xd':'~/conary/src/xfce-devel/','fl2':'~/conary/src/fl2-devel/'}
contexts = {'xd':'xfce:devel','fl2':'fl:2-devel'}
pkglists = {'xd':'pkglist_xd','fl2':'pkglist_fl'}

def wipe_out(dir):
    dir = os.path.expanduser(dir)
#    print 'delete ',dir
    sp.check_call(['rm','-rf',dir])
    
def chdir(dir):
    dir = os.path.expanduser(dir)
#    print 'change directory:',dir
    os.chdir(dir)

def needsupdate_git(subrepo, project, gitrepo):
    repo = pkglist.subrepos[subrepo]
    srcname = repo[project]
    try: # don't update ig git or conary fails
        curgit = cpk.request_query(project+":source", ilp)[0][1].trailingRevision().getVersion()
    except:
        return False
    print 'latest version of ' + project + ' in conary is: ' + curgit
    try:
        newgit =    sp.Popen(['git', 'ls-remote', '-h', gitrepo+subrepo+'/'+srcname, 'master'],
            stdout=sp.PIPE, stderr=sp.STDOUT).stdout.read().strip()
    except:
        return False
    newgit = newgit[:7]
    print 'latest commit of ' + project + ' in git is: ' + newgit
    return (newgit != curgit)

def needsbuild(project):
    try: # no need to build if no source is available
        srev = cpk.request_query(project +':source', ilp)[0][1].trailingRevision()
    except:
        return False
    try: # build if no binary available
        brev = cpk.request_query(project, ilp)[0][1].trailingRevision()
    except:
        return True
    #print srev,srev.buildCount,srev.sourceCount, brev,brev.buildCount,brev.sourceCount
    return (srev.getVersion() != brev.getVersion() or
            srev.sourceCount != brev.sourceCount)

def refresh(project):
    print 'refresh: ' + project
    wipe_out(codir + project)
    chdir(codir)
    cvc.main(['refresh-xfce.py','co',project + '=' + ilp])
    chdir(codir + project)
    cvc.main(['refresh-xfce.py','refresh'])
    cvc.main(['refresh-xfce.py','ci', '--no-interactive', "-m'sync with upstream'"])
    chdir(cwd)
    
def update():
    for s in pkglist.subrepos:
        for p in pkglist.subrepos[s]:
            if needsupdate_git(s,p,gitrepo):
                refresh(p)
    
def build():
    rmakecl = ['refresh-xfce.py', 'build',]
    for s in pkglist.subrepos:
        for p in pkglist.subrepos[s]:
            if buildall or needsbuild (p):
                rmakecl.append(p + '{x86_64}')
                rmakecl.append(p + '{x86}')
    rmakecl.append('--context='+contexts[options.repo])
    rmakecl.append ('--commit')
    print rmakecl
    rmk.main(rmakecl)
    
parser = OptionParser(usage ="usage: %prog [options] action\n"
                      "\nActions:\n"
                      "  update\t\tUpdate source\n"
                      "  build\t\t\tbuild package\n"
                      "  buildall\t\tbuild all packages",
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
pkglist = __import__(pkglists[options.repo])
if (args[0] == 'update'):
    update()
elif (args[0] == 'build'):
    buildall = False
    build()
elif (args[0] == 'buildall'):
    buildall = True
    build()
elif (args[0] == 'all'):
    update()
    build()
else:
    parser.error("argument not allowed")
