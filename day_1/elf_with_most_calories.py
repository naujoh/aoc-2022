"""
    Advent of Code 2022 | puzzle day 1
    puzzle link: https://adventofcode.com/2022/day/1
"""


def get_elfs_calories(elf_top: int) -> int:
    elf_most_cal = [0 for _ in range(elf_top)]
    elf_cal_count = 0

    with open('input.txt') as f:
        for line in f:
            cal_item = line.strip()
            if cal_item:
                elf_cal_count += int(cal_item)
            else:
                update_elf_cal_list(elf_most_cal, elf_cal_count)
                elf_cal_count = 0
        if elf_cal_count:
            update_elf_cal_list(elf_most_cal, elf_cal_count)

    print(f'Top {elf_top} elfs carrying most calories: {elf_most_cal}')
    return sum(elf_most_cal)


def update_elf_cal_list(elf_calories: list, elf_cal_count: int) -> None:
    min_idx = elf_calories.index(min(elf_calories))
    elf_calories[min_idx] = elf_cal_count


if __name__ == '__main__':
    elf_most_cal = get_elfs_calories(elf_top=1)
    print(f'The elf carrying most calories is carrying: {elf_most_cal} cal.')

    top_3_elfs_cal = get_elfs_calories(elf_top=3)
    print(
        f'The total calories of the top 3 elfs carrying most calories is: '
        f' {top_3_elfs_cal} cal.')
