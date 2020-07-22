'''Modul contains File Manager class to handle various task using os module'''

import os


class FileManager:
    '''File Manager class handling varous tasks on files and folders

    Attributes:
        root_dir(str): Path object, path of the root directory.

    Methods:
        find_files: Return the list of files matching regular expression
    '''
    def __init__(self, root_dir=None):
        if not root_dir:
            self.root = os.getcwd()
        else:
            assert os.path.exists(root_dir) and os.path.isdir(root_dir), \
            'root_dir need to be existing path to directory.'
            self.root = root_dir

    def find_files(suffix, path):
        """
        Find all files beneath path with file name suffix.

        Note that a path may contain further subdirectories
        and those subdirectories may also contain further subdirectories.

        There are no limit to the depth of the subdirectories can be.

        Args:
          suffix(str): suffix if the file name to be found
          path(str): path of the file system

        Returns:
           a list of paths
        """
        return paths
