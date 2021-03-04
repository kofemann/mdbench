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

License
-------

Public Domain

How to contribute
-----------------

**mdbench** uses the linux kernel model where git is not only source repository,
but also the way to track contributions and copyrights.

Each submitted patch must have a "Signed-off-by" line.  Patches without
this line will not be accepted.

The sign-off is a simple line at the end of the explanation for the
patch, which certifies that you wrote it or otherwise have the right to
pass it on as an open-source patch.  The rules are pretty simple: if you
can certify the below:

```txt
    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
         have the right to submit it under the open source license
         indicated in the file; or

    (b) The contribution is based upon previous work that, to the best
        of my knowledge, is covered under an appropriate open source
        license and I have the right under that license to submit that
        work with modifications, whether created in whole or in part
        by me, under the same open source license (unless I am
        permitted to submit under a different license), as indicated
        in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including all
        personal information I submit with it, including my sign-off) is
        maintained indefinitely and may be redistributed consistent with
        this project or the open source license(s) involved.
```

then you just add a line saying ( git commit -s )

```txt
Signed-off-by: Random J Developer <random@developer.example.org>
```

using your real name (sorry, no pseudonyms or anonymous contributions.)
