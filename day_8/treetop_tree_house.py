"""
    Advent of Code 2022 | puzzle day 8
    puzzle link: https://adventofcode.com/2022/day/8
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class TreeGrid:
    trees: List[List[int]] = field(default_factory=lambda: [])
    columns: int = 0
    rows: int = 0
    visible_trees: int = field(default=0, init=False)
    highest_scenic_score: int = field(default=0, init=False)

    def add_row(self, row: List[int]) -> None:
        self.trees.append(row)
        self.rows += 1
        if self.columns <= 0:
            self.columns = len(row)

    def traverse(self) -> None:
        self.visible_trees = self.columns * 2 + self.rows * 2 - 4
        last_col_idx = self.columns - 1
        last_row_idx = self.rows - 1

        for r in range(self.rows):
            for c in range(self.columns):
                ignore_item = (
                    (c == 0 or c == last_col_idx) or
                    (r == 0 or r == last_row_idx))
                if ignore_item:
                    continue

                if self.is_tree_visible(self.trees[r][c], (r, c)):
                    self.visible_trees += 1
                t_scenic_score = self \
                    .calculate_tree_scenic_score(self.trees[r][c], (r, c))
                if self.highest_scenic_score < t_scenic_score:
                    self.highest_scenic_score = t_scenic_score

    # First part
    def is_tree_visible(self, tree: int, tree_pos: tuple) -> bool:
        is_visible = True

        for side, sibling_range in self.get_tree_siblings(tree_pos).items():
            for t in range(*sibling_range):
                sibling_tree = self.trees[tree_pos[0]][t]
                if side == 't' or side == 'b':
                    sibling_tree = self.trees[t][tree_pos[1]]
                if sibling_tree >= tree:
                    is_visible = False
                    break
            if is_visible:
                return is_visible
            is_visible = True

        return False

    # Second part
    def calculate_tree_scenic_score(self, tree: int, tree_pos: tuple) -> int:
        scenic_score = 0
        for side, sibling_range in self.get_tree_siblings(tree_pos).items():
            trees_seeing = 0
            for t in range(*sibling_range):
                sibling_tree = self.trees[tree_pos[0]][t]
                if side == 't' or side == 'b':
                    sibling_tree = self.trees[t][tree_pos[1]]
                if sibling_tree >= tree:
                    trees_seeing += 1
                    break
                trees_seeing += 1
            scenic_score = (scenic_score * trees_seeing
                            if scenic_score > 0 else trees_seeing)
        return scenic_score

    def get_tree_siblings(self, tree_pos: tuple) -> dict:
        return {
            'l': [tree_pos[1]-1, -1, -1],
            'r': [tree_pos[1]+1, self.columns],
            't': [tree_pos[0]-1, -1, -1],
            'b': [tree_pos[0]+1, self.rows]}


def main():
    tree_grid = TreeGrid()

    with open('input.txt', 'r') as f:
        for line in f:
            tree_grid.add_row(list(map(lambda t: int(t), line.strip())))

    tree_grid.traverse()
    print(f'Trees per row: {tree_grid.columns}\n'
          f'Trees rows count: {tree_grid.rows}')
    print(f'Visible trees: {tree_grid.visible_trees}')
    print(f'Highest scenic score in grid: {tree_grid.highest_scenic_score}')


if __name__ == '__main__':
    main()
