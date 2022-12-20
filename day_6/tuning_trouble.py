"""
    Advent of Code 2022 | puzzle day 6
    puzzle link: https://adventofcode.com/2022/day/6
"""
from dataclasses import dataclass

PACKET_MARKER_SIZE = 4
MESSAGE_MARKER_SIZE = 14


@dataclass
class Marker:
    size: int
    value: str = ''
    idx_last_char_added: int = 0

    def add_char(self, char_idx: int, char: str) -> None:
        if char_idx < self.size:
            self.value += char
        elif self.size == len(self.value):
            self.value = f'{self.value[1::]}{char}'
        self.idx_last_char_added = char_idx + 1

    def is_valid(self) -> bool:
        if len(self.value) < self.size:
            return False
        return len(set(self.value)) == self.size


def main() -> None:
    with open('input.txt', 'r') as f:
        for line in f:
            packet_marker = Marker(PACKET_MARKER_SIZE)
            message_marker = Marker(MESSAGE_MARKER_SIZE)
            for i, c in enumerate(line):
                if not packet_marker.is_valid():
                    packet_marker.add_char(i, c)

                if not message_marker.is_valid():
                    message_marker.add_char(i, c)

                if packet_marker.is_valid() and message_marker.is_valid():
                    print(f'First packet marker detected after character '
                          f'{packet_marker.idx_last_char_added}')
                    print(f'First message marker detected after character '
                          f'{message_marker.idx_last_char_added}')
                    break


if __name__ == '__main__':
    main()
