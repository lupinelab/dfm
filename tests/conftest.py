import pytest
from unittest.mock import patch

@pytest.fixture()
def profile_dir(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("profile")
    tmpdir.join("mydotfile.txt").ensure()
    yield tmpdir

@pytest.fixture()
def dotfile(profile_dir):
    df = profile_dir.join(".bashrc")
    df.ensure()
    yield df

@pytest.fixture()
def home_dir(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("home")
    with patch("os.path.expanduser", return_value=tmpdir):
        yield tmpdir