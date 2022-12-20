"""
    Advent of Code 2022 | puzzle day 3
    puzzle link: https://adventofcode.com/2022/day/3
"""
import string

ITEMS_PRIORITY_DICTIONARY = {l: i+1 for i, l
                             in enumerate(string.ascii_letters)}
ELFS_GROUP_SIZE = 3


def get_common_item_in_compartments(items: str) -> str:
    '''
        Function written to solve 1st part of the puzzle
    '''
    common_item = None
    items_registry = dict()
    items_per_compartment = int(len(items)/2)
    for i, item in enumerate(items):
        if not items_registry.get(item):
            item_count = [0, 0]
            if i + 1 <= items_per_compartment:
                item_count[0] += 1
            else:
                item_count[1] += 1

            items_registry[item] = item_count
        else:
            if i + 1 <= items_per_compartment:
                items_registry[item][0] += 1
            else:
                items_registry[item][1] += 1
        if items_registry[item][0] > 0 and items_registry[item][1] > 0:
            common_item = item
            break
    if not common_item:
        raise ValueError('Cannot find common item in items list')
    return common_item


def get_common_item_in_sets(items: str, sets_boundaries: list) -> str:
    '''
        Rewritten function of 1st part of the puzzle to solve
        all puzzles parts.
    '''
    if not sets_boundaries:
        raise ValueError('Cannot get common item on only one set.')
    common_item = ''
    items_registry = dict()
    sets_quantity = len(sets_boundaries) + 1
    set_transversed = 0

    for i, item in enumerate(items):
        if item not in items_registry:
            item_count = [0 for _ in range(0, sets_quantity)]
            if i + 1 <= sets_boundaries[set_transversed]:
                item_count[set_transversed] += 1
            else:
                item_count[set_transversed+1] += 1
            items_registry[item] = item_count
        else:
            if i + 1 <= sets_boundaries[set_transversed]:
                items_registry[item][set_transversed] += 1
            else:
                items_registry[item][set_transversed+1] += 1
        # If item of the next iteration is in another set then update the
        # set transversed variable
        if (i + 2 > sets_boundaries[set_transversed]
                and set_transversed + 1 < len(sets_boundaries)):
            set_transversed += 1
        # Avoid to check if common item found if is not the last set
        if i + 1 <= sets_boundaries[set_transversed]:
            continue
        item_found = False
        for count in items_registry[item]:
            if count < 1:
                item_found = False
                break
            item_found = True
        if item_found:
            common_item = item
            break
    if not common_item:
        raise ValueError('Cannot find common item in items list')
    return common_item


def main() -> None:
    priority_sum, elf_group_priority_sum = 0, 0
    with open('input.txt') as f:
        elf_count = 1
        elf_group_items = ''
        elf_group_boundaries = []
        for items in f:
            _items = items.strip()
            # Puzzle part 1
            sets_boundaries = [int(len(_items)/2)]
            common_item = get_common_item_in_sets(
                items.strip(), sets_boundaries)
            priority_sum += ITEMS_PRIORITY_DICTIONARY[common_item]

            # Puzzle part 2
            elf_group_items += _items
            if not elf_count % ELFS_GROUP_SIZE:
                elf_group_common_item = get_common_item_in_sets(
                    elf_group_items, elf_group_boundaries)
                elf_group_priority_sum += ITEMS_PRIORITY_DICTIONARY[
                    elf_group_common_item]
                elf_group_items = ''
                elf_group_boundaries = []
            else:
                elf_group_boundaries.append(len(elf_group_items))
            elf_count += 1
    print(f'Sum of priority for common items is: {priority_sum}')
    print(f'Sum of priority for common items of elfs groups is: '
          f'{elf_group_priority_sum}')


if __name__ == '__main__':
    main()
