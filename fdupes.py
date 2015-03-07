#!/usr/bin/env python

import hashlib
import os
import sys

DIR_DELIM='\\'

DELCOMMAND="del"

def pathtofiles(s):
        ret = list()
        for dir,subdirs,files in os.walk(s):
                for filename in files:
                        ret.append(dir+DIR_DELIM+filename)
        return ret

def checksizes(arr):
        sizes = dict()
        for f in arr:
                try:
                        size = os.path.getsize(f)
                        if size > 1024*1024 and size not in sizes.keys():
                                sizes[size]=list()
                        sizes[size].append(f)
                except:
                        pass
        samesizes = dict()
        for size in sizes.keys():
                if len(sizes[size])>1:
                        samesizes[size] = sizes[size]
        return samesizes

def checksums(files):

        ret = dict()

        for filename in files:
                try:
                        file = open( filename,'rb' )
                        hashop = hashlib.md5()
                        hashop.update(file.read(1024*1024))
                        digest = hashop.hexdigest()
                        if digest not in ret.keys():
                                ret[digest] = list()
                        ret[digest].append(filename)
                except:
                        pass

        return ret

dupes = list()
print "Searching",sys.argv[1]
arrayoffiles = pathtofiles(sys.argv[1])
print "Found",len(arrayoffiles),"files"
samesize = checksizes(arrayoffiles)
print len(samesize),"have the same size"
f = open("""%UserProfile%\Desktop\samesize.txt""",'w')
for size in samesize.keys():
        checksummed = checksums(samesize[size])
        for hash in checksummed.keys():
                if len(checksummed[hash])>1:
                        f.write("\n".join(checksummed[hash]) + "\n")
                        f.write("="*5 + "\n")
                        dupes.append( min(checksummed[hash]) )

dupes.sort()
for dupe in dupes:
        print DELCOMMAND,'"'+dupe+'"'
sys.exit()

