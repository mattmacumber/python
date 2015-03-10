#!/usr/bin/env python

import collections
import hashlib
import os
import sys

DELCOMMAND = "del"


def pathtofiles(search_dir):
    """Given a directory, return a list of the full path to all files"""
    ret = list()
    for dir, subdirs, files in os.walk(search_dir):
        for filename in files:
            ret.append(os.sep.join((dir, filename)))
    return ret


def checksizes(file_list, min_size=(1024 * 1024)):
    """Given a list of files, return a dict with
    key: file size
    value: a list of files of that size
    """
    sizes = collections.defaultdict(list)
    for filename in file_list:
        try:
            size = os.path.getsize(filename)
            sizes[size].append(filename)
        except:
            pass

    samesizes = dict()
    for size in sizes.keys():
        if len(sizes[size]) > 1:
            samesizes[size] = sizes[size]
    return samesizes


def checksums(files, file_sample_size=(1024 * 1024)):

    ret = dict()

    for filename in files:
        try:
            file = open(filename, 'rb')
            hashop = hashlib.md5()
            hashop.update(file.read(file_sample_size))
            digest = hashop.hexdigest()
            if digest not in ret.keys():
                ret[digest] = list()
            ret[digest].append(filename)
        except:
            pass

    return ret

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Need a directory to search"
        sys.exit(-1)
    else:
        directory = sys.argv[1]

    dupes = list()

    print "Searching {0}".format(directory)
    file_list = pathtofiles(directory)

    print "Found {0} files".format(len(file_list))
    samesize = checksizes(file_list)

    print "{0} files have the same size".format(len(samesize))

    f = open("""%UserProfile%\Desktop\samesize.txt""", 'w')
    for size in samesize.keys():
        checksummed = checksums(samesize[size])
        for hash in checksummed.keys():
            if len(checksummed[hash]) > 1:
                f.write("\n".join(checksummed[hash]))
                f.write("\n")
                f.write("=" * 5)
                f.write("\n")
                dupes.append(min(checksummed[hash]))

    dupes.sort()
    for dupe in dupes:
        print "{0} \"{1}\"".format(DELCOMMAND, dupe)
