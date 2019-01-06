import pytest
import os
import shutil

from cpr import api

data_dir = os.path.join(os.path.dirname(__file__), 'data', 'bzip2-1.0.6-h1de35cc_5')


@pytest.fixture(scope='function')
def testing_workdir(tmpdir, request):
    """ Create a workdir in a safe temporary folder; cd into dir above before test, cd out after

    :param tmpdir: py.test fixture, will be injected
    :param request: py.test fixture-related, will be injected (see pytest docs)
    """

    saved_path = os.getcwd()

    tmpdir.chdir()
    # temporary folder for profiling output, if any
    tmpdir.mkdir('prof')

    def return_to_saved_path():
        if os.path.isdir(os.path.join(saved_path, 'prof')):
            profdir = tmpdir.join('prof')
            files = profdir.listdir('*.prof') if profdir.isdir() else []

            for f in files:
                shutil.copy(str(f), os.path.join(saved_path, 'prof', f.basename))
        os.chdir(saved_path)

    request.addfinalizer(return_to_saved_path)

    return str(tmpdir)


@pytest.fixture(scope='function')
def prefix_with_files_recorded(testing_workdir, request):
    for entry in os.listdir(data_dir):
        if os.path.isdir(os.path.join(data_dir, entry)):
            shutil.copytree(os.path.join(data_dir, entry), os.path.join(testing_workdir, entry))
    api.replace_paths(testing_workdir, os.path.join(testing_workdir, 'info', 'has_prefix'))
    return testing_workdir
