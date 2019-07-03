#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright (C) 2013-2019 Deutsches Elektronen-Synchroton,
# Member of the Helmholtz Association, (DESY), HAMBURG, GERMANY
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#

'''
Simple filesystem metadata operations benchmark

Usage: mdbench [options] <PATH>

  where options are:
    -f, --files <N>  : number of generated files per directory
    -d, --dirs  <N>  : number of generated directories to generate
    -s, --size  <N>  : size of generated files in B/K/M/G
    -n, --no-clean   : do not delete created files and directories
    --no-container   : do not create the 'mdbench.<name>.<pid>' directory
    -h, --help       : help message

  and PATH points to the directory where tests should run. Current directory
  is used if not specified.

If number of generated directories is 0 then files are created within
the container directory ("mdbench.<name>.<pid>") or in PATH if
--no-container is specified.

The file size can be specified in human friendly format, e.g.: 1K, 256M. 4G.
'''

from __future__ import division
import sys
import os
import socket
import getopt
import string
from datetime import datetime
import numpy as np

DIR = 'dir.'
FILE = 'file.'

gen_dir = lambda base, gen : '%s/%s%d' % (base, DIR, gen)
gen_file = lambda base, gen : '%s/%s%d' % (base, FILE, gen)

B = 1
K = 1024
M = K*K
G = K*M

DATA_SIZES = {'b':B, 'k': K, 'm': M, 'g': G}


dir_creates = []
file_creates = []
file_stats = []
dir_stats = []
dir_removes = []
file_removes = []

def get_size(s):

	last_symbol = s[-1:].lower()
	if last_symbol in string.digits:
		return long(s)

	if not DATA_SIZES.has_key(last_symbol):
		raise Exception('Invalid format: %s' % s)

	return long(s[:-1])*DATA_SIZES[last_symbol]

def make_dirs(root, count):
	for i in range(count):
		mkdir( gen_dir(root, i) )

def make_files(root, dir_count, file_count, size = 0):
	for j in range(file_count):
		if dir_count > 0:
			for i in range(dir_count):
				mkfile(gen_file( gen_dir(root, i), j ), size, 1024)
		else:
			mkfile(gen_file(root, j), size, 1024)

def del_files(root, dir_count, file_count):
	for j in range(file_count):
		if dir_count > 0:
			for i in range(dir_count):
				rmfile(gen_file( gen_dir(root, i), j ))
		else:
			rmfile(gen_file(root, j))

def del_dirs(root, count):
	for i in range(count):
		rmdir( gen_dir(root, i) )

def stat_dirs(root, count):
	for i in range(count):
		statdir( gen_dir(root, i) )

def stat_files(root, dir_count, file_count):
	for j in range(file_count):
		if dir_count > 0:
			for i in range(dir_count):
				statfile(gen_file( gen_dir(root, i), j ))
		else:
			statfile(gen_file(root, j))

def rmfile(f):
	start = datetime.now()
	os.remove(f)
	end = datetime.now()
	file_removes.append(total_micros(end - start))

def rmdir(d):
	start = datetime.now()
	os.rmdir(d)
	end = datetime.now()
	dir_removes.append(total_micros(end - start))

def mkdir(d):
	start = datetime.now()
	os.mkdir(d)
	end = datetime.now()
	dir_creates.append(total_micros(end - start))

def statfile(f):
	start = datetime.now()
	os.stat(f)
	end = datetime.now()
	file_stats.append(total_micros(end - start))

def statdir(f):
	start = datetime.now()
	os.stat(f)
	end = datetime.now()
	dir_stats.append(total_micros(end - start))

def mkfile(fname, size = 0, chunk = 65536, sync = False) :
	n_chunks = size // chunk

	bite = bytearray(chunk)
	payload = bytearray(size % chunk)

	start = datetime.now()
	with open(fname, "wb") as f:
		for n in range(n_chunks) :
			f.write(bite)

		f.write(payload)
		if sync:
			f.flush()
			os.fsync(f.fileno())

	end = datetime.now()
	file_creates.append(total_micros(end - start))

def total_micros(td):
	return td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6

def report(title, raw):
	data = np.array(raw)
	print('{:16}: {:6.2f}μ ±{:=6.2f}μ, {:6.2f} op/s' \
		.format(title, np.mean(data), np.std(data), len(raw)/np.sum(data)*10**6))

DIR_COUNT = 1000
FILE_COUNT = 10
FILE_SIZE = 0

def usage():
	print(__doc__)
	sys.exit(1)

def main():

	dir_count = DIR_COUNT
	file_count = FILE_COUNT
	file_size = FILE_SIZE
	cleanup = True
	createContainer = True

	try:
		options, remainder = getopt.gnu_getopt(sys.argv[1:], 'f:d:s:nh', \
					 ['files=','dirs=','size=','no-clean','no-container','help'])
	except getopt.GetoptError as err:
		print(str(err))
		usage()

	for opt, arg in options:
		if opt in ('-f', '--files'):
			file_count = int(arg)
		elif opt in ('-d', '--dirs'):
			dir_count = int(arg)
		elif opt in ('-s', '--size'):
			file_size = get_size(arg)
		elif opt in ('-n', '--no-clean'):
			cleanup = False
		elif opt in ('--no-container'):
			createContainer = False
		elif opt in ('-h', '--help'):
			usage()

	if len(remainder) != 1 :
		usage()

	path = remainder[0]

	root = '%s/mdbench.%s.%d' % (path, socket.gethostname(), os.getpid()) if createContainer else path

	if createContainer:
		os.mkdir(root)

	make_dirs(root, dir_count)
	report("dir creates", dir_creates)
	make_files(root, dir_count, file_count , file_size)
	report("file creates", file_creates)
	stat_files(root, dir_count, file_count)
	report("file stats", file_stats)
	stat_dirs(root, dir_count)
	report("dir stats", dir_stats)

	if cleanup:
		del_files(root, dir_count, file_count )
		report("file removes", file_removes)
		del_dirs(root, dir_count )
		report("dir removes", dir_removes)
		if createContainer:
			os.rmdir(root)

if __name__ == '__main__':
	main()
