"""
    Advent of Code 2022 | puzzle day 4
    puzzle link: https://adventofcode.com/2022/day/4
"""


def main():
    assignments_pairs_fully_contained = 0
    assignment_pairs_overlaped = 0
    with open('input.txt') as f:
        for line in f:
            assignment_pairs = line.strip()
            assignment_pairs = assignment_pairs.split(',')
            a1, b1 = assignment_pairs[0].split('-')
            a2, b2 = assignment_pairs[1].split('-')
            a1, b1, a2, b2 = int(a1), int(b1), int(a2), int(b2)
            if (a1 >= a2 and b1 <= b2) or (a2 >= a1 and b2 <= b1):
                assignments_pairs_fully_contained += 1
                assignment_pairs_overlaped += 1
            elif(a1 <= a2 and b1 >= a2) or (a2 <= a1 and b2 >= a1):
                assignment_pairs_overlaped += 1

    print(f'Assigment pairs fully contained in other: '
          f'{assignments_pairs_fully_contained}')
    print(f'Overlaped assignments pairs: '
          f'{assignment_pairs_overlaped}')


if __name__ == '__main__':
    main()
