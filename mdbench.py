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

DIR = 'dir.'
FILE = 'file.'

gen_dir = lambda base, gen : '%s/%s%d' % (base, DIR, gen)
gen_file = lambda base, gen : '%s/%s%d' % (base, FILE, gen)

B = 1
K = 1024
M = K*K
G = K*M

DATA_SIZES = {'b':B, 'k': K, 'm': M, 'g': G}

def get_size(s):

	last_symbol = s[-1:].lower()
	if last_symbol in string.digits:
		return long(s)

	if not DATA_SIZES.has_key(last_symbol):
		raise Exception('Invalid format: %s' % s)

	return long(s[:-1])*DATA_SIZES[last_symbol]

def make_dirs(root, count):
	for i in range(count):
		os.mkdir( gen_dir(root, i) )

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
				os.remove(gen_file( gen_dir(root, i), j ))
		else:
			os.remove(gen_file(root, j))

def del_dirs(root, count):
	for i in range(count):
		os.rmdir( gen_dir(root, i) )

def stat_dirs(root, count):
	for i in range(count):
		os.stat( gen_dir(root, i) )

def stat_files(root, dir_count, file_count):
	for j in range(file_count):
		if dir_count > 0:
			for i in range(dir_count):
				os.stat(gen_file( gen_dir(root, i), j ))
		else:
			os.stat(gen_file(root, j))


def mkfile(fname, size = 0, chunk = 65536, sync = False) :
	n_chunks = size // chunk

	bite = bytearray(chunk)
	payload = bytearray(size % chunk)

	with open(fname, "wb") as f:
		for n in range(n_chunks) :
			f.write(bite)

		f.write(payload)
		if sync:
			f.flush()
			os.fsync(f.fileno())

def total_seconds(td):
	return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

def bench_run(func, *args):
	start = datetime.now()

	result = func(*args)

	end = datetime.now()
	elapsed = end - start

	return elapsed, result

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

	elapsed, result = bench_run( make_dirs, root, dir_count )
	in_sec = total_seconds(elapsed)
	print('%.2f dir creates per second' % (dir_count/in_sec))

	elapsed, result = bench_run( make_files, root, dir_count, file_count , file_size)
	in_sec = total_seconds(elapsed)
	count = (dir_count if dir_count > 0 else 1) * file_count
	print('%.2f file creates per second' % (count/in_sec))

	elapsed, result = bench_run( stat_files, root, dir_count, file_count )
	in_sec = total_seconds(elapsed)
	print('%.2f file stats per second' % (count/in_sec))

	if cleanup:
		elapsed, result = bench_run( del_files, root, dir_count, file_count )
		in_sec = total_seconds(elapsed)
		print('%.2f file removes per second' % (count/in_sec))

		elapsed, result = bench_run( del_dirs, root, dir_count )
		in_sec = total_seconds(elapsed)
		print('%.2f dir removes per second' % (dir_count/in_sec))

		if createContainer:
			os.rmdir(root)

if __name__ == '__main__':
	main()
