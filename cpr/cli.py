from argparse import ArgumentParser

from cpr import api


def cli(args):
    p = ArgumentParser(
        description="""
Tool for replacing hard-coded prefixes in text and binary files""",
        conflict_handler='resolve'
    )
    sp = p.add_subparsers(title='subcommands', dest='subparser_name')
    detect_parser = sp.add_parser('detect', help='detect hard-coded prefixes in files', aliases=['d'])
    detect_parser.add_argument("prefix", help="base prefix of files to replace prefixes in.  This is "
                               "the local location on disk.")
    detect_parser.add_argument("--files", help="Path to file specifying subset of files within prefix to examine.  "
                               "File should contain one relative path per line.")
    detect_parser.add_argument("--extra_paths", nargs="+", help="Additional paths relative to the "
                               "prefix that should also be detected and recorded.  For example, "
                               "../_build_env may be useful if the build env has been recorded in files.")
    detect_parser.add_argument("--out-path", default="has_prefix", help="path to file to save detected paths to.  "
                               "Path must be provided for CLI usage (default is has_prefix).  For API usage, "
                               "defaults to None, and you get the list of results instead.")

    replace_parser = sp.add_parser('replace', help='replace hard-coded prefixes in files with new value', aliases=['r'])
    replace_parser.add_argument("prefix", help="base prefix of files to replace prefixes in.  This is "
                               "the local location on disk.")
    replace_parser.add_argument("--paths_file", default='has_prefix', help="text file listing files that need "
                                "replacement attention.  Format is: FILE_PATH PATH_EMBEDDING_TYPE PATH_TO_BE_REPLACED.  "
                                "See any package's info/has_prefix file for examples.")
    args, = p.parse_args(args)

    if args.subparser_name in ('detect', 'd'):
        api.detect_paths(args.prefix, args.files, args.extra_paths, args.out_path)

    elif args.subparser_name in ('replace', 'r'):
        api.replace_paths(args.prefix, args.recorded_paths)


if __name__ == '__main__':
    import sys
    cli(sys.argv[1:])
