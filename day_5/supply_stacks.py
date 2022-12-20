"""
    Advent of Code 2022 | puzzle day 5
    puzzle link: https://adventofcode.com/2022/day/5
"""
import re
import copy
from dataclasses import dataclass


@dataclass
class Instruction:
    qty_to_move: int
    source_stack: int
    target_stack: int


def main() -> None:
    with open('input.txt', 'r') as f:
        reading_movements = False
        crates_arrangement = dict()
        for line in f:
            line = line.strip()

            if line == '#':
                reading_movements = True
                crates_arrangement_c = copy.deepcopy(crates_arrangement)
                continue
            if not reading_movements:
                crates_stack_num, crates_stack = line.split(' ')
                crates_stack = crates_stack.split(',')
                crates_arrangement[int(crates_stack_num)] = crates_stack
            else:
                instruction = get_arrangement_instruction(line)
                perform_rearrangement(instruction, crates_arrangement, '9000')
                perform_rearrangement(
                    instruction, crates_arrangement_c, '9001')
        top_cages_by_stack_cm9000 = ''.join(
            [v[-1] for _, v in crates_arrangement.items()])
        top_cages_by_stack_cm9001 = ''.join(
            [v[-1] for _, v in crates_arrangement_c.items()])
        print(f'Top cages by stack CM-9000: {top_cages_by_stack_cm9000}')
        print(f'Top cages by stack CM-9001: {top_cages_by_stack_cm9001}')


def perform_rearrangement(i: Instruction, arrangement: dict,
                          crate_mover_version: str) -> None:
    if crate_mover_version == '9001':
        stack_to_update = arrangement[i.source_stack]
        cages_to_move = stack_to_update[
            len(stack_to_update)-i.qty_to_move::]
        arrangement[i.target_stack] += cages_to_move
        arrangement[i.source_stack] = stack_to_update[0:len(
            stack_to_update)-i.qty_to_move]
        return

    for _ in range(0, i.qty_to_move):
        arrangement[i.target_stack].append(
            arrangement[i.source_stack].pop())


def get_arrangement_instruction(raw_instruction: str) -> Instruction:
    instruction = re.sub(r'move | from| to', '', raw_instruction)
    instruction = instruction.split(' ')
    instruction = [int(e) for e in instruction]
    instruction = Instruction(
        qty_to_move=instruction[0],
        source_stack=instruction[1],
        target_stack=instruction[2])
    return instruction


if __name__ == '__main__':
    main()
