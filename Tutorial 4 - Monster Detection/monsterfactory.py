from monster import Monster


class MonsterFactory:
    def __init__(self):
        self.count = 0

    def create_monster(self, monster_type):
        monster = Monster(monster_type)
        self.count = self.count + 1
        return monster
