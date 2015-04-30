import os
import sys

listen_filenames = sys.argv[1:]

listen_files = list()
for fname in listen_filenames:
        with open(fname) as f:
                listen_files += [ line.strip() for line in f.readlines() ]

library_files = dict()
for root, dirs, files in os.walk('./'):
        for f in files:
                if f.endswith('.mp3'):
                        library_files[f] = root+'/'+f

new_files = set(library_files) - set(listen_files)
new_files = sorted([library_files[f] for f in new_files])

print "Listend to {0} files".format(len(listen_files))
print "{0} files in the library".format(len(library_files))
print "New File Count {0}".format(len(new_files))

print '\n'.join(new_files)
