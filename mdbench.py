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

import os
import socket
from datetime import datetime

DIR = 'dir.'
FILE = 'file.'

gen_dir = lambda base, gen : '%s/%s%d' % (base, DIR, gen)
gen_file = lambda base, gen : '%s/%s%d' % (base, FILE, gen)

def make_dirs(root, count):
	for i in range(count):
		os.mkdir( gen_dir(root, i) )

def make_files(root, dir_count, file_count):
	for i in range(dir_count):
		for j in range(file_count):
			f = open(gen_file( gen_dir(root, i), j ), 'w')
			f.close()

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


def bench_run(func, *args):
	start = datetime.now()

	result = func(*args)

	end = datetime.now()
	elapsed = end - start

	return elapsed, result


if __name__ == '__main__':
	
	dir_count = 1000
	file_count = 10
	root = 'mdbench.%s.%d' % (socket.gethostname(), os.getpid())

	os.mkdir(root)
	elapsed, result = bench_run( make_dirs, root, dir_count )
	in_sec = elapsed.total_seconds()
	print '%.2f dir creates per second' % (dir_count/in_sec)

	elapsed, result = bench_run( make_files, root, dir_count, file_count )
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
