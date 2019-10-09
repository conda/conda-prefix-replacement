# conda-prefix-replacement
CPR resuscitates packages in new locations. It's a library for detecting files
that have the prefix baked into them, and also for replacing those baked-in
prefixes with new values when files are moved.

```
usage: cpr [-h] [-V] {detect,d,replace,r,rehome} ...

Tool for replacing hard-coded prefixes in text and binary files

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Show the conda-prefix-replacement version number and
                        exit.

subcommands:
  {detect,d,replace,r,rehome}
    detect (d)          detect hard-coded prefixes in files
    replace (r)         replace hard-coded prefixes in files with new value
    rehome              fix a moved installation by changing embedded paths to
                        match the new location
```

Most people probably just want `rehome`, which combines the `detect` and
`replace` functions. For example, say you copy your Anaconda installation from
/Anaconda3 to ~/anaconda3. You can fix the embedded paths by running:

`cpr rehome ~/anaconda3`

That finds your old prefix by looking in some files that are known to record the
prefix in a readily parseable way. If that fails, you can still fix things as
long as you know what the original path was:

`cpr rehome ~/anaconda3 --old-prefix /Anaconda3`

The detect and replace commands are more for conda/conda-build usage.
Conda-build detects files that have the prefix at build time, so that those
prefixes can be replaced by conda at install time.
