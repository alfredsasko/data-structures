'''Modul contains File Manager class to handle various file system tasks'''

import os
import pathlib
from concurrent.futures import ThreadPoolExecutor
from collections import deque
import re


class FileManager:
    '''File Manager class handling varous tasks on files and folders

    Methods:
        find_files: Return the list of files matching regular expression
    '''

    def find_files(self, path, query, regex=False, max_workers=10):
        """Find all files beneath path with matching query.

        Note that a path may contain further subdirectories
        and those subdirectories may also contain further subdirectories.

        There are no limit to the depth of the subdirectories can be.

        Args:
          query(str): string to match file path
          path(str or pathlib.Path): path of the file system
          regex(bool): Indicator if query is regular expression. Default False.
          max_workers: Maximum number of the threads, 10 by default

        Returns:
           a list of paths
        """

        # Initiate concurrent breath first search using threads
        futures = deque()
        files = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures.append(executor.submit(
                self._find_files, path, query, regex))
            while futures:
                future = futures.popleft()

                # Raise if thread return exception
                if future.exception():
                    raise future.exception()

                # If thread is completed extend found files and start
                # new threads for each subdirectory
                elif future.done():
                    subdirs, found_files = future.result()
                    files.extend(found_files)
                    for subdir in subdirs:
                        futures.append(
                            executor.submit(
                                self._find_files, subdir, query, regex))

                # If thread not finished yet, place thread at the end
                # of the queue
                else:
                    futures.append(future)

        return files

    def _find_files(self, path, query, regex=False):
        '''Returns list of querying files in specified directory (path) and
        list of child directories. Method is used for internal purposes and is
        wrapped into multi-threading interface to return files from whole
        directory tree.
        '''

        assert isinstance(query, str), 'Query needs to be string.'
        assert isinstance(path, (str, pathlib.Path)), \
        'Path needs to be str or pathlib.Path object.'

        path = pathlib.Path(path) if isinstance(path, str) else path

        assert path.is_dir(), 'Directory not found in {}'.format(os.getcwd())

        if regex:
            query = re.compile(query)

        subdirs, files = [], []
        for p in path.iterdir():

            if p.is_dir() and not p.is_symlink():
                subdirs.append(p)

            if p.is_file():
                file_path = p.as_posix()

                if ((regex and query.match(file_path))
                    or ((not regex) and (query in file_path))):

                    files.append(file_path)

        return subdirs, files
