"""
    Advent of Code 2022 | puzzle day 9
    puzzle link: https://adventofcode.com/2022/day/9
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Set, Tuple, Optional


@dataclass
class Instruction:
    direction: str
    steps: int


@dataclass
class Rope:
    length: int
    length_without_head: int = field(init=False)
    knots: List[Knot] = field(init=False, default_factory=lambda: [])

    def __post_init__(self) -> None:
        if self.length <= 0:
            raise ValueError('Cannot create rope without knots.')
        for _ in range(0, self.length - 1):
            self.knots.append(Knot(x=0, y=0))
        # Append tail with tracking coordinates at the end
        self.knots.append(Knot(x=0, y=0, coordinates_history={(0, 0)}))
        self.length_without_tail = self.length - 1

    def get_head(self) -> Knot:
        return self.knots[0]

    def get_tail(self) -> Knot:
        return self.knots[-1]

    def move(self, instruction: Instruction) -> None:
        for _ in range(0, instruction.steps):
            self.get_head().move(instruction.direction)
            self._move_knots(instruction)

    def _move_knots(self, instruction: Instruction) -> None:
        knot_idx = 0
        # Move each knot of rope to the next position
        while knot_idx < self.length_without_tail:
            head, tail = self.knots[knot_idx:knot_idx+2]
            knots_overlap = head.x == tail.x and head.y == tail.y
            if not self.are_knots_adjacent(head, tail) and not knots_overlap:
                tail.move(instruction.direction, head)
            knot_idx += 1

    def are_knots_adjacent(self, knot1: Knot, knot2: Knot) -> bool:
        # TODO rewrite this method to reduce avoid check each adjacent
        # position, instead use the postions of each knot to check possible
        # adjacent spots.
        are_adjacent = False
        # Go through all possible adjacent postions
        for delta_x in range(-1, 2, 1):
            for delta_y in range(-1, 2, 1):
                x = knot1.x + delta_x
                y = knot1.y + delta_y
                if x == knot2.x and y == knot2.y:
                    are_adjacent = True
                    break
        return are_adjacent


@dataclass
class Knot:
    x: int
    y: int
    coordinates_history: Optional[Set[Tuple[int, int]]] = None

    def move(self, direction: str, head: Knot = None) -> None:
        if not head:
            if direction == 'R':
                self.x += 1
            if direction == 'L':
                self.x -= 1
            if direction == 'U':
                self.y += 1
            if direction == 'D':
                self.y -= 1
            self.save_coordinate(self.x, self.y)
            return

        if self.x != head.x and self.y != head.y:
            self._move_diagonally(head)
            self.save_coordinate(self.x, self.y)
            return

        # Move knot through "y" axis
        if self.x == head.x:
            self.y = head.y - 1 if self.y < head.y else head.y + 1
        # Move knot through "x" axis
        elif self.y == head.y:
            self.x = head.x - 1 if self.x < head.x else head.x + 1
        else:
            raise ValueError('Knots are not alligned at same row or col.')
        self.save_coordinate(self.x, self.y)

    def _move_diagonally(self, head: Knot) -> None:
        # knot at left-bottom of head
        knot_x = self.x + 1
        knot_y = self.y + 1

        # knot at right of head
        if self.x > head.x:
            knot_x = self.x - 1
        # knot at top of head
        if self.y > head.y:
            knot_y = self.y - 1

        self.x = knot_x
        self.y = knot_y

        self.save_coordinate(self.x, self.y)

    def save_coordinate(self, x: int, y: int) -> None:
        if self.coordinates_history is None:
            return
        coordinate = (x, y)
        if coordinate not in self.coordinates_history:
            self.coordinates_history.add(coordinate)

    def get_visited_positions_count(self) -> int:
        if self.coordinates_history is None:
            raise ValueError('Coordinates history not stored for knot.')
        return len(self.coordinates_history)


def main() -> None:
    rope = Rope(length=2)
    long_rope = Rope(length=10)

    with open('input.txt', 'r') as f:
        for line in f:
            direction, steps = line.strip().split(' ')
            instruction = Instruction(direction, int(steps))
            # Firts part
            rope.move(instruction)
            # Second part
            long_rope.move(instruction)

    print(f'Number of visited positions of the tail: '
          f'{rope.get_tail().get_visited_positions_count()}')
    print(f'Number of visited position of tail (long rope): '
          f'{long_rope.get_tail().get_visited_positions_count()}')


if __name__ == '__main__':
    main()
