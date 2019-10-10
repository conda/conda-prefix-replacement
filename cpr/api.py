import os as _os

from six import string_types as _string_types


def detect_paths(prefix, path_to_detect=None, files=None, extra_paths=None, out_path=None):
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

    if not path_to_detect:
        path_to_detect = prefix

    if not _os.path.isabs(prefix):
        old_prefix = _os.path.join(_os.getcwd(), prefix)

    detected_content = detect_prefix_files(prefix, path_to_detect, files, extra_paths)

    if out_path:
        folder_name = _os.path.dirname(out_path)
        if folder_name and not _os.path.isdir(folder_name):
            _os.makedirs(_os.path.dirname(out_path))
        with open(out_path, 'w') as f:
            for entry in detected_content:
                f.write('    '.join(entry) + "\n")
    else:
        return detected_content


def replace_paths(prefix, recorded_paths):
    """Given a list of paths in a prefix, go in and do the text or binary replacement
    of hard-coded prefixes"""
    from cpr.replacement import update_prefix

    if not _os.path.isabs(prefix):
        old_prefix = _os.path.join(_os.getcwd(), prefix)

    if isinstance(recorded_paths, _string_types):
        if not _os.path.isfile(recorded_paths):
            raise ValueError("File given for list of recorded paths, '{}', does not appear to exist".format(recorded_paths))
        with open(recorded_paths) as f:
            recorded_paths = (_.split() for _ in f.readlines())
    for (placeholder, mode, path) in recorded_paths:
        if placeholder != prefix:
            try:
                update_prefix(path, prefix, placeholder, mode)
            except OSError:
                print("error with path {}".format(path))


def rehome(prefix, old_prefix=None):
    """Given a prefix that represents a folder that has been moved from another location,
    attempt to "rehome" it - find instances of the old prefix baked into files, and adjust
    those baked-in locations to match the new location."""
    import sys
    import re
    if not _os.path.isabs(prefix):
        prefix = _os.path.join(_os.getcwd(), prefix)
    if not old_prefix:
        if sys.platform == "win32":
            raise NotImplementedError
        else:
            # openssl is pretty omnipresent.  This file has a path entry (not a shebang) that we can use
            #   Shebangs are not good because they can become /usr/bin/env things if path gets too long
            trial_paths = (
                'lib/pkgconfig/liblzma.pc',
                'lib/pkgconfig/tk.pc',
                'lib/pkgconfig/ncursesw.pc',
            )
            for path in trial_paths:
                abspath = _os.path.join(prefix, path)
                if _os.path.isfile(abspath):
                    with open(abspath) as f:
                        match = re.search("^prefix=(.*)$", f.read(), re.M)
                        if match:
                            old_prefix = match.group(1)
                            break

    if not old_prefix:
        raise ValueError("No known prefix files were found in your environment.  Can't auto-detect "
                         "old prefix.  Please specify it manually with the --old-prefix argument.")

    if not _os.path.isabs(old_prefix):
        old_prefix = _os.path.join(_os.getcwd(), old_prefix)

    detected_paths = detect_paths(prefix, old_prefix)
    replace_paths(prefix, detected_paths)

