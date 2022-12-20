"""
    Advent of Code 2022 | puzzle day 7
    puzzle link: https://adventofcode.com/2022/day/7
"""
from __future__ import annotations
from typing import Optional, List, Dict
from dataclasses import dataclass, field


@dataclass
class Directory:
    parent: Optional[Directory]
    name: str
    child_dirs: Dict[str, Directory] = field(init=False)
    files: List[File] = field(init=False)

    def __post_init__(self):
        self.child_dirs = {}
        self.files = []

    def add_child_dir(self, directory: Directory):
        self.child_dirs[directory.name] = directory

    def add_child_file(self, file: File):
        self.files.append(file)

    def get_directory_size(self):
        files_size = sum(f.size for f in self.files)
        childs_dirs_size = sum(
            dir.get_directory_size() for dir in self.child_dirs.values())
        return files_size + childs_dirs_size


@dataclass
class File:
    parent: Directory
    name: str
    size: int


class FileSystemMapper:
    PROMT_CHAR = '$'
    CHANGE_DIR_INSTRUCTION = '$ cd'
    LIST_DIR_INSTRUCTION = '$ ls'
    DIR_ITEM_IDENTIFIER = 'dir'
    BACK_DIRECTORY_INSTRUCTION = '..'
    FS_TOTAL_SIZE = 70_000_000

    root_dir: Optional[Directory] = None
    cwd: Optional[Directory] = None

    def process_line(self, line: str) -> None:
        if line.startswith(self.CHANGE_DIR_INSTRUCTION):
            dirname = line.split(' ')[2]
            self.cwd = self.change_dir(dirname, self.cwd)
        elif line.startswith(self.DIR_ITEM_IDENTIFIER):
            dirname = line.split(' ')[1]
            self.add_dir(dirname, self.cwd)
        elif not line.startswith(self.LIST_DIR_INSTRUCTION):
            size, name = line.split(' ')
            self.add_file(name, int(size), self.cwd)

    def add_file(
            self, filename: str, size: int, parent: Directory = None) -> None:
        if not parent:
            raise ValueError('Cannot identify the current working '
                             'directory to add item.')
        file = File(parent, filename, size)
        parent.add_child_file(file)

    def add_dir(self, dir_name: str, parent: Directory = None) -> Directory:
        new_dir = Directory(parent, dir_name)
        if parent and not parent.child_dirs.get(dir_name):
            parent.add_child_dir(new_dir)
        if not self.root_dir:
            self.root_dir = new_dir
        return new_dir

    def change_dir(self, dirname: str, cwd: Directory = None) -> Directory:
        if dirname == self.BACK_DIRECTORY_INSTRUCTION:
            if not cwd:
                raise ValueError(
                    'Current working directory is not defined')
            if not cwd.parent:
                raise ValueError(
                    'Cannot change directory backwards, '
                    'root dir reached!')
            return cwd.parent
        if cwd and cwd.child_dirs.get(dirname):
            return cwd.child_dirs[dirname]
        return self.add_dir(dirname, cwd)

    def get_directories_sizes(self, dir: Directory, dir_list: list = None):
        if dir_list is None:
            dir_list = []

        for c_dir in dir.child_dirs.values():
            self.get_directories_sizes(c_dir, dir_list)

        dir_list.append((dir.name, dir.get_directory_size()))

        return dir_list

    def get_unused_space(self) -> int:
        if not self.root_dir:
            raise ValueError('Cannot find root dir.')
        return self.FS_TOTAL_SIZE - self.root_dir.get_directory_size()


def main():
    fs = FileSystemMapper()
    with open('input.txt', 'r') as f:
        for line in f:
            fs.process_line(line.strip())
    if not fs.root_dir:
        return
    dir_sizes = fs.get_directories_sizes(fs.root_dir)

    # Part one
    dir_sizes_sum = sum(
        map(lambda d: d[1], filter(lambda d: d[1] <= 100000, dir_sizes)))
    print(f'Total sum of dirs with size <= 100000: {dir_sizes_sum}')

    # Part two
    storage_required_for_update = 30_000_000
    fs_unused_space = fs.get_unused_space()
    if fs_unused_space >= storage_required_for_update:
        print('Update can be perform, there is enough disk space available')
        return
    size_of_dir_to_remove = min(
        map(lambda d: d[1], filter(
            lambda d: d[1] + fs_unused_space >= storage_required_for_update,
            dir_sizes)))
    print(f'Size of dir that can be deleted to freeup enough disk space '
          f'for update is: {size_of_dir_to_remove}')


if __name__ == '__main__':
    main()
