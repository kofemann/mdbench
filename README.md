mdbench
=======

Simple filsystem metadata operations benchmark
----------------------------------------------
```
Usage: mdbench [options] [PATH]

  where options are:
    -f, --files <N>  : number of generated files per directory
    -d, --dirs  <N>  : number of generated directories to generate
    -s, --size  <N>  : size of generated files in B/K/M/G
    -n, --no-clean   : do not delete created files and directories
    -h, --help       : help message

  and PATH points to a directory where the test should run. Currect directory is
  used of not specified.
  
The file size can be specified in human friendly format, e.g.: 1K, 256M. 4G.
```

```sh
$ mdbench.py -d 1 -f 1000 -s 1 /net/dcache/exports/data
dir creates     : 6001.00μ ±  0.00μ, 166.64 op/s
file creates    : 16448.76μ ±3926.05μ,  60.79 op/s
file stats      : 373.97μ ±163.12μ, 2674.01 op/s
dir stats       : 395.00μ ±  0.00μ, 2531.65 op/s
file removes    : 1823.41μ ±1139.57μ, 548.42 op/s
dir removes     : 3556.00μ ±  0.00μ, 281.21 op/s
```
