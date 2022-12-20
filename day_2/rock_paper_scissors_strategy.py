"""
    Advent of Code 2022 | puzzle day 2
    puzzle link: https://adventofcode.com/2022/day/2
"""
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Shape:
    id: str
    alt_id: str
    value: int


@dataclass
class GameRule:
    shape: Shape
    win_against: Shape
    lose_against: Shape


@dataclass
class GameResult:
    id: str
    granted_points: int = 0


@dataclass
class GameManager:
    rock: Shape = Shape('A', 'X', 1)
    paper: Shape = Shape('B', 'Y', 2)
    scissors: Shape = Shape('C', 'Z', 3)

    lose: GameResult = GameResult('X')
    draw: GameResult = GameResult('Y', 3)
    win: GameResult = GameResult('Z', 6)

    rules: Dict[str, GameRule] = field(init=False)

    def __post_init__(self):
        self.rules = {
            self.rock.id: GameRule(
                self.rock, win_against=self.scissors, lose_against=self.paper),
            self.paper.id: GameRule(
                self.paper, win_against=self.rock, lose_against=self.scissors),
            self.scissors.id: GameRule(
                self.scissors, win_against=self.paper, lose_against=self.rock)}

    def play(
            self, opponent_s: str, player_s: str = '', needed_res: str = None):
        o_rule = self.rules[opponent_s]
        """
            Part 1 - Opponent and Player results given
            Game round possible results
            rock: 1, paper: 2, scissors: 3
            ---
            shape - shape: 0 -> 3 [draw]
            1 - 3: -2 -> lose
            1 - 2: -1 -> win
            2 - 3: -1 -> win
            2 - 1: 1 -> lose
            3 - 2: 1 -> lose
            3 - 1: 2 -> win
        """
        if not needed_res:
            p_rule = self.get_player_rule_by_alt_name(player_s)
            shape_diff = o_rule.shape.value - p_rule.shape.value
            if not shape_diff:
                return p_rule.shape.value + self.draw.granted_points
            elif shape_diff == -1 or shape_diff == 2:
                return p_rule.shape.value + self.win.granted_points
            else:
                return p_rule.shape.value
        """
            Part 2 - Opponent and required results given
            rock: 1, paper: 2, scissors: 3
            X: should lose = 1, Y: should draw = 2, Z: should win = 3
        """
        if needed_res == self.lose.id:
            return o_rule.win_against.value
        elif needed_res == self.win.id:
            return o_rule.lose_against.value + self.win.granted_points
        else:
            return o_rule.shape.value + self.draw.granted_points

    def get_player_rule_by_alt_name(self, shape_id: str) -> GameRule:
        for _, rule in self.rules.items():
            if rule.shape.alt_id == shape_id:
                return rule
        raise ValueError(
            f'Cannot find a shape with alternative id: {shape_id}')


def main():
    total_score, total_score2 = 0, 0
    gm = GameManager()
    with open('input.txt') as f:
        for line in f:
            shape, required_res = line.split()
            total_score += gm.play(opponent_s=shape, player_s=required_res)
            total_score2 += gm.play(opponent_s=shape,
                                    needed_res=required_res)

    print(f'Total score: {total_score}')
    print(f'Total score right strategy: {total_score2}')


if __name__ == '__main__':
    main()
