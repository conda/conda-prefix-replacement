import os
import shutil
from cpr import api
from cpr.detection import codec

data_dir = os.path.join(os.path.dirname(__file__), 'data', 'bzip2-1.0.6-h1de35cc_5')


def _find_in_file(file_path, text):
    if hasattr(text, 'encode'):
        text = text.encode(codec)
    with open(file_path, 'rb+') as fi:
        mm = fi.read()
    return mm.find(text) != -1


def test_detect_paths(prefix_with_files_recorded):
    """NOTE: this test depends heavily on prefix replacement already working.  That's because the formulation
    of this test uses prefix replacement from a known package to change prefixes to something that we know
    detection should work on."""
    detected_paths = list(api.detect_paths(prefix_with_files_recorded))
    assert len(detected_paths) == 4
    assert detected_paths[0][0] == prefix_with_files_recorded


def test_update_prefixes(testing_workdir):
    for entry in os.listdir(data_dir):
        if os.path.isdir(os.path.join(data_dir, entry)):
            shutil.copytree(os.path.join(data_dir, entry), os.path.join(testing_workdir, entry))

    with open(os.path.join(testing_workdir, 'info', 'has_prefix')) as f:
        placeholder, ftype, fn = f.readline().split()

    # initially, testing_workdir shouldn't be part of the file
    assert not _find_in_file(os.path.join(testing_workdir, fn), testing_workdir)
    assert _find_in_file(os.path.join(testing_workdir, fn), placeholder)
    api.replace_paths(testing_workdir, os.path.join(testing_workdir, 'info', 'has_prefix'))
    assert _find_in_file(os.path.join(testing_workdir, fn), testing_workdir)
    assert not _find_in_file(os.path.join(testing_workdir, fn), placeholder)

    detected_paths = list(api.detect_paths(testing_workdir))
    assert len(detected_paths) == 4
