#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright (C) 2013 Deutsches Elektronen-Synchroton,
# Member of the Helmholtz Association, (DESY), HAMBURG, GERMANY
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#

'''mdbench

Simple filsystem metadata operations benchmark

'''

import sys
import os
import socket
import getopt
from datetime import datetime

DIR = 'dir.'
FILE = 'file.'

gen_dir = lambda base, gen : '%s/%s%d' % (base, DIR, gen)
gen_file = lambda base, gen : '%s/%s%d' % (base, FILE, gen)

def make_dirs(root, count):
	for i in range(count):
		os.mkdir( gen_dir(root, i) )

def make_files(root, dir_count, file_count, size = 0):
	for i in range(dir_count):
		for j in range(file_count):
			mkfile(gen_file( gen_dir(root, i), j ), 1024, size)

def del_files(root, dir_count, file_count):
	for i in range(dir_count):
		for j in range(file_count):
			os.remove(gen_file( gen_dir(root, i), j ))

def del_dirs(root, count):
	for i in range(count):
		os.rmdir( gen_dir(root, i) )

def stat_dirs(root, count):
	for i in range(count):
		os.stat( gen_dir(root, i) )

def stat_files(root, dir_count, file_count):
	for i in range(dir_count):
		for j in range(file_count):
			os.stat(gen_file( gen_dir(root, i), j ))

def mkfile(fname, size = 0, chunk = 1024, sync = False) :
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

def bench_run(func, *args):
	start = datetime.now()

	result = func(*args)

	end = datetime.now()
	elapsed = end - start

	return elapsed, result


if __name__ == '__main__':
	
	dir_count = 1000
	file_count = 10
	file_size = 0

	options, remainder = getopt.gnu_getopt(sys.argv[1:], 'f:d:s:')
	for opt, arg in options:
		if opt in ('-f'):
			file_count = int(arg)
		elif opt in ('-d'):
			dir_count = int(arg)
		elif opt in ('-s'):
			file_size = long(arg)

	root = 'mdbench.%s.%d' % (socket.gethostname(), os.getpid())

	os.mkdir(root)
	elapsed, result = bench_run( make_dirs, root, dir_count )
	in_sec = elapsed.total_seconds()
	print '%.2f dir creates per second' % (dir_count/in_sec)

	elapsed, result = bench_run( make_files, root, dir_count, file_count , file_size)
	in_sec = elapsed.total_seconds()
	print '%.2f files creates per second' % ((dir_count*file_count)/in_sec)

	elapsed, result = bench_run( stat_files, root, dir_count, file_count )
	in_sec = elapsed.total_seconds()
	print '%.2f files stats per second' % ((dir_count*file_count)/in_sec)

	elapsed, result = bench_run( del_files, root, dir_count, file_count )
	in_sec = elapsed.total_seconds()
	print '%.2f files removes per second' % ((dir_count*file_count)/in_sec)

	elapsed, result = bench_run( del_dirs, root, dir_count )
	in_sec = elapsed.total_seconds()
	print '%.2f dir removes per second' % (dir_count/in_sec)

	os.rmdir(root)
