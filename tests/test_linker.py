import os

from dfm.linking.linker import Linker
from dfm.linking.ignore import Ignore


def test_make_path_relative():
    linker = Linker("a", "b", Ignore([]), [])

    abs_path = "/home/jedrw/something.txt"
    relative_to = "/home/jedrw"

    expected_path = "something.txt"

    result = linker.make_path_relative(abs_path, relative_to)

    assert result == expected_path
    

def test_link_to_homedir(dotfile, home_dir):
    linker = Linker("a", "b", Ignore([]), [])

    linker.link_to_homedir(dotfile, dotfile.basename)
    
    assert os.path.exists(home_dir.join(dotfile.basename))
    assert os.path.islink(home_dir.join(dotfile.basename))