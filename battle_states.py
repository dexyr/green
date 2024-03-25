"""
state machine for handling battles
"""

from __future__ import annotations

from typing import Optional, Type

from bearlibterminal import terminal

from data import Globals, Unit, Attack, Teams
from battle_util import Constants, TextDisplay, Menu, Field, Timeline


# i think all the BattleSubState type-hints should be Type[BattleSubState] but
#  maybe the IDE isn't picking up on all of them


class BattleState:
    @classmethod
    def switch(cls) -> Type[BattleState]:
        pass

    @classmethod
    def logic(cls) -> Optional[Type[BattleState]]:
        pass

    @classmethod
    def render(cls) -> None:
        pass


class BattleSubState:
    @classmethod
    def logic(cls) -> Optional[Type[BattleState]]:
        pass

    @classmethod
    def render(cls) -> None:
        pass

    @classmethod
    def text_logic(cls) -> bool:
        if TextDisplay.done:
            return True
        if terminal.TK_ENTER in Globals.keys:
            TextDisplay.update_text()
            return False
        return False


class Start(BattleState):
    class Init(BattleSubState):
        @classmethod
        def logic(cls) -> Optional[Type[BattleState]]:
            Field.add_units(Globals.party, Globals.enemies)
            Timeline.add_units(Globals.party, Globals.enemies)
            TextDisplay.add_texts(
                ['battle start! right now! totally happening!'])
            Start.sub_state = Start.Text
            return

        @classmethod
        def render(cls) -> None:
            pass

    class Text(BattleSubState):
        @classmethod
        def logic(cls) -> Optional[Type[BattleState]]:
            if cls.text_logic():
                return Limbo.switch()

        @classmethod
        def render(cls) -> None:
            TextDisplay.render()

    sub_state: Type[BattleSubState] = Init

    @classmethod
    def logic(cls) -> Optional[Type[BattleState]]:
        return cls.sub_state.logic()

    @classmethod
    def render(cls) -> None:
        Field.render(Timeline.current_unit)
        Timeline.render(0)
        cls.sub_state.render()


class Actions(BattleState):
    index_action: int = 0

    @classmethod
    def switch(cls) -> Optional[Type[BattleState]]:
        Actions.index_action = 0
        return cls

    @classmethod
    def logic(cls) -> Optional[Type[BattleState]]:
        for k in Globals.keys:
            if k in [terminal.TK_UP, terminal.TK_DOWN,
                     terminal.TK_LEFT, terminal.TK_RIGHT]:

                Actions.index_action = Menu.get_new_selection(
                    k, cls.index_action, len(Constants.ACTIONS))
                return

            if k == terminal.TK_ENTER:
                action: Constants.ACTIONS =\
                    Constants.ACTIONS[cls.index_action]

                if action == Constants.ACTIONS[0]:  # scuffed enum
                    return cls.choose_attack()

                if action == Constants.ACTIONS[1]:
                    print('re-move-d lol')
                    return

                if action == Constants.ACTIONS[2]:
                    print('use item')
                    return

                if action == Constants.ACTIONS[3]:
                    print('retreat')
                    return

                assert False  # lmao how'd this happen

    @classmethod
    def choose_attack(cls) -> Optional[Type[BattleState]]:
        return Attacks.switch()

    @classmethod
    def render(cls) -> None:
        Field.render(Timeline.current_unit)
        Timeline.render(0)
        Menu.render(Constants.ACTIONS, cls.index_action)


class Attacks(BattleState):
    class Menu(BattleSubState):
        @classmethod
        def logic(cls) -> Optional[Type[BattleState]]:
            for k in Globals.keys:
                if k in [terminal.TK_UP, terminal.TK_DOWN,
                         terminal.TK_LEFT, terminal.TK_RIGHT]:

                    Attacks.index_attack = Menu.get_new_selection(
                        k,
                        Attacks.index_attack,
                        len(Timeline.current_unit.attacks))
                    return

                if k == terminal.TK_ENTER:
                    Attacks.index_target = Field.get_closest_target()
                    Attacks.sub_state = Attacks.Target
                    return

                if k == terminal.TK_ESCAPE:
                    return Actions.switch()

        @classmethod
        def render(cls) -> None:
            Menu.render(
                [a.attack_type.name for a in Timeline.current_unit.attacks],
                Attacks.index_attack)
            Timeline.render(0)

    class Target(BattleSubState):
        @classmethod
        def logic(cls) -> Optional[Type[BattleState]]:
            for k in Globals.keys:
                if k in [terminal.TK_UP, terminal.TK_DOWN]:
                    Attacks.index_target = Field.change_target(
                        Attacks.index_target, k)
                    return

                if k == terminal.TK_ENTER:
                    result = Field.do_attack(
                        Timeline.current_unit,
                        Attacks.index_attack,
                        Attacks.index_target)

                    Timeline.apply_delay(Attacks.index_attack)
                    TextDisplay.add_texts([result])
                    Attacks.sub_state = Attacks.Confirm
                    return

                if k == terminal.TK_ESCAPE:
                    Attacks.sub_state = Attacks.Menu
                    return

        @classmethod
        def render(cls) -> None:
            current_unit: Unit = Timeline.current_unit

            Menu.render(
                [a.attack_type.name for a in Timeline.current_unit.attacks],
                Attacks.index_attack)
            Field.draw_selected_target(Attacks.index_target)

            attack: Attack = current_unit.attacks[Attacks.index_attack]
            Timeline.render(attack.attack_type.delay)

    class Confirm(BattleSubState):
        @classmethod
        def logic(cls) -> Optional[Type[BattleState]]:
            if cls.text_logic():
                return Limbo.switch()

        @classmethod
        def render(cls) -> None:
            Field.draw_selected_target(Attacks.index_target)

            current_unit: Unit = Timeline.current_unit
            attack: Attack = current_unit.attacks[Attacks.index_attack]
            Timeline.render(attack.attack_type.delay)

            TextDisplay.render()

    sub_state: Type[BattleSubState] = Menu
    index_attack: int = 0
    index_target: int = -1

    @classmethod
    def switch(cls) -> Optional[Type[BattleState]]:
        Attacks.index_attack = 0
        Attacks.index_target = 0
        cls.sub_state = cls.Menu
        return cls

    @classmethod
    def logic(cls) -> Optional[Type[BattleState]]:
        return cls.sub_state.logic()

    @classmethod
    def render(cls) -> None:
        Field.render(Timeline.current_unit)
        cls.sub_state.render()


class Item(BattleState):
    @classmethod
    def logic(cls) -> Optional[Type[BattleState]]:
        return

    @classmethod
    def render(cls) -> None:
        return


class Retreat(BattleState):
    @classmethod
    def logic(cls) -> Optional[Type[BattleState]]:
        return

    @classmethod
    def render(cls) -> None:
        return


class Enemy(BattleState):
    class AI(BattleSubState):
        index_attack: int = 0
        index_target: int = -1

        @classmethod
        def find_target(cls):
            for t in Timeline.current_unit.unit_type.target_types:
                target_index: int = Field.get_index(
                    lambda u: u.unit_type.name == t, Teams.PLAYER)
                if target_index != -1:
                    return target_index
            assert False  # for now just like, don't; lol

        @classmethod
        def logic(cls) -> Optional[Type[BattleState]]:
            Enemy.AI.index_target = cls.find_target()

            result = Field.do_attack(
                Timeline.current_unit,
                Enemy.AI.index_attack,
                Enemy.AI.index_target)

            Timeline.apply_delay(Enemy.AI.index_attack)
            TextDisplay.add_texts([result])
            Enemy.sub_state = Enemy.Confirm
            return

        @classmethod
        def render(cls) -> None:
            pass

    class Confirm(BattleSubState):
        @classmethod
        def logic(cls) -> Optional[Type[BattleState]]:
            if cls.text_logic():
                return Limbo.switch()

        @classmethod
        def render(cls) -> None:
            TextDisplay.render()
            Field.draw_selected_target(Enemy.AI.index_target)

    sub_state: Type[BattleSubState] = AI

    @classmethod
    def switch(cls) -> Optional[Type[BattleState]]:
        cls.sub_state = cls.AI
        return cls

    @classmethod
    def logic(cls) -> Optional[Type[BattleState]]:
        return cls.sub_state.logic()

    @classmethod
    def render(cls) -> None:
        Field.render(Timeline.current_unit)
        Timeline.render(0)
        cls.sub_state.render()


class Limbo(BattleState):
    class Process(BattleSubState):
        @classmethod
        def logic(cls) -> Optional[Type[BattleState]]:
            if dead := Timeline.get_unit(lambda u: u.hp <= 0):
                Timeline.battle_units.pop(
                    Timeline.get_index(lambda u: u is dead))

                dead_index: int = Field.get_index(lambda u: u is dead, None)
                Field.positions[dead_index].unit = None
                TextDisplay.add_texts([f'{dead.unit_type.name} died!'])
                Limbo.sub_state = Limbo.Confirm
                return

            party = Field.get_units_by_team(Teams.PLAYER)
            enemies = Field.get_units_by_team(Teams.ENEMY)

            if not party or not enemies:
                return End.switch()

            if Timeline.battle_units[0].battle_delay > 0:
                #      ^ this is a special case
                Timeline.update_tick()
                # do any DoT-type effects here
                return

            Timeline.current_unit = Timeline.battle_units[0]
            TextDisplay.add_texts(
                [f'it\'s {Timeline.current_unit.unit_type.name}\'s turn!'])
            Limbo.sub_state = Limbo.Change
            return

        @classmethod
        def render(cls) -> None:
            pass

    class Confirm(BattleSubState):
        @classmethod
        def logic(cls) -> Optional[Type[BattleState]]:
            if cls.text_logic():
                Limbo.sub_state = Limbo.Process
                return

        @classmethod
        def render(cls) -> None:
            TextDisplay.render()

    class Change(BattleSubState):
        @classmethod
        def logic(cls) -> Optional[Type[BattleState]]:
            if cls.text_logic():
                if Timeline.current_unit.unit_type.team == Teams.PLAYER:
                    return Actions.switch()
                else:
                    return Enemy.switch()

        @classmethod
        def render(cls) -> None:
            TextDisplay.render()

    sub_state: Type[BattleSubState] = Process

    @classmethod
    def switch(cls) -> Optional[Type[BattleState]]:
        cls.sub_state = cls.Process
        return cls

    @classmethod
    def logic(cls) -> Optional[Type[BattleState]]:
        return cls.sub_state.logic()

    @classmethod
    def render(cls) -> None:
        Field.render(Timeline.current_unit)
        Timeline.render(0)
        cls.sub_state.render()


class End(BattleState):
    class Init(BattleSubState):
        @classmethod
        def logic(cls) -> None:
            TextDisplay.add_texts(['the battle is over!'])
            End.sub_state = End.Text

        @classmethod
        def render(cls) -> None:
            pass

    class Text(BattleSubState):
        @classmethod
        def logic(cls) -> None:
            pass

        @classmethod
        def render(cls) -> None:
            TextDisplay.render()

    sub_state = Init

    @classmethod
    def switch(cls) -> Type[BattleState]:
        return cls

    @classmethod
    def logic(cls) -> Optional[Type[BattleState]]:
        return cls.sub_state.logic()

    @classmethod
    def render(cls) -> None:
        Field.render(None)
        Timeline.render(0)
        cls.sub_state.render()
