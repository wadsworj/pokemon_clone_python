from events.pick_monster_event import PickMonsterEvent
from events.prof_pick_monster_event import ProfPickMonsterEvent


def handle_prof_event(game, player, npc):
    if len(player.monsters) != 0:
        return

    event = ProfPickMonsterEvent(game.screen, game, player)
    game.event = event

def handle_pick_monster_event(game, player, npc):
    if len(player.monsters) != 0:
        return

    event = PickMonsterEvent(game.screen, game, player, npc)
    game.event = event

def handle(game, player, npc):
    player.position = player.last_position

    if npc.name == 'prof':
        handle_prof_event(game, player, npc)

    if npc.name.startswith("monster_cage_starter_"):
        handle_pick_monster_event(game, player, npc)

    pass