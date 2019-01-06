import os as _os

from six import string_types as _string_types


def detect_paths(prefix, files=None, extra_paths=None, out_path=None):
    """Detect instances of 'prefix' embedded in files within that prefix

    files: if provided, limits the subset of files within prefix that are examined.

    extra_paths: can be a string or list of strings. These should be paths
        relative to the prefix. For example, in conda-build, the prefix will be the
        host env, _h_env_placehold..., but sometimes the build prefix gets embedded
        because that's where compilers are.  You can pass '../_build_env' to extra_paths
        to detect instances of that also.

    out_path: if provided, this function will write a file with the path data
        to this path. It will clobber files, but it will error out if the path
        provided is an already-existing folder."""

    from cpr.detection import detect_prefix_files

    if isinstance(files, _string_types):
        with open(files) as f:
            files = f.readlines()

    detected_content = detect_prefix_files(prefix, files, extra_paths)

    if out_path:
        if not _os.path.isdir(_os.path.basedir(out_path)):
            _os.makedirs(_os.path.basedir(out_path))
        with open(out_path, 'w') as f:
            for entry in detected_content:
                print('    '.join(entry), file=f)
    else:
        return detected_content


def replace_paths(prefix, recorded_paths):
    """Given a list of paths in a prefix, go in and do the text or binary replacement
    of hard-coded prefixes"""
    from cpr.replacement import update_prefix
    if not _os.path.isfile(recorded_paths):
        raise ValueError("File given for list of recorded paths, '{}', does not appear to exist".format(recorded_paths))
    with open(recorded_paths) as f:
        for entry in f.readlines():
            placeholder, mode, path = entry.split()
            update_prefix(path, prefix, placeholder, mode)
