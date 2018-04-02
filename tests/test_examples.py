import contextlib
import glob
import os
import StringIO
import sys
import tempfile

import pytest
from mock import mock

from ldraw import download_main, library_gen_main, try_write_lib


@pytest.fixture
def mocked_parts_lst():
    parts_lst_path = os.path.join('tmp', 'ldraw', 'parts.lst')
    download_main(parts_lst_path)
    with mock.patch('ldraw.get_config', side_effect=lambda: {'parts.lst': parts_lst_path}):
        try_write_lib()
        yield parts_lst_path


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


examples_dir = 'examples'
all_examples = [os.path.splitext(os.path.basename(s))[0] for s in glob.glob(os.path.join(examples_dir, '*.py'))]


def exec_example(name, save=False):
    script_file = os.path.join(examples_dir, '%s.py' % name)

    d = dict(locals(), **globals())

    with stdoutIO() as s:
        execfile(script_file, d, d)
    content = s.getvalue()
    expected_path = os.path.join('tests', 'test_data', 'examples', '%s.ldr' % name)
    # uncomment to save
    # open(expected_path, 'w').write(content)

    expected = open(expected_path, 'r').read()
    assert expected == content


@pytest.mark.parametrize('example', all_examples, ids=all_examples)
def test_examples(mocked_parts_lst, example):
    exec_example(example)
