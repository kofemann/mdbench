mdbench
=======

Simple filsystem metadata operations benchmark
----------------------------------------------

Usage: mdbench [options]

  where options are:
    -f, --files <N>  : number of generated files per directory
    -d, --dirs  <N>  : number of generated directories to generate
    -s, --size  <N>  : size of generated files in B/K/M/G
    -p, --path <dir> : directory where the test should run
    -h, --help       : helpl message

The file size can be specified in human friendly format, e.g.: 1K, 256M. 4G.

```sh
$ ./mdbench.py -d 10 -p /mnt/exports/data/
46236.36 dir creates per second
12963.49 files creates per second
36035.65 files stats per second
33829.84 files removes per second
46262.03 dir removes per second
$ 
```
