from argparse import ArgumentParser
import os

from cpr import replacement


def cli(args):
    p = ArgumentParser(
        description="""
Tool for replacing hard-coded prefixes in text and binary files""",
        conflict_handler='resolve'
    )
    p.add_argument("prefix", help="base prefix of files to replace prefixes in.  This is "
                   "the local location on disk.")
    p.add_argument("paths_file", help="text file listing files that need replacement attention."
                   " Format is: FILE_PATH PATH_EMBEDDING_TYPE PATH_TO_BE_REPLACED.  "
                   "See any package's info/has_prefix file for examples.")
    args, = p.parse_args(args)
    with open(args.paths_file) as f:
        for line in f.readlines():
            placeholder, mode, relative_path = line.split()
            file_path = os.path.join(args.prefix, relative_path)
            replacement.update_prefix(file_path, args.prefix, placeholder, mode)


if __name__ == '__main__':
    import sys
    cli(sys.argv[1:])
