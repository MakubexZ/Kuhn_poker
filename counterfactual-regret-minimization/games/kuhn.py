from common.constants import CHECK, BET, CALL, FOLD, A, CHANCE, RESULTS_MAP
import random

class GameStateBase:

    def __init__(self, parent, to_move, actions, n):
        self.parent = parent
        self.to_move = to_move
        self.actions = actions
        self.n = n

    def play(self, action):
        # print('play this action', action)
        # print('children[action]', self.children[action])
        return self.children[action]

    def is_chance(self):
        return self.to_move == CHANCE

    def inf_set(self):
        raise NotImplementedError("Please implement information_set method")

class KuhnRootChanceGameState(GameStateBase):
    #   print(GameStateBase)
    def __init__(self, actions):
        # print(actions)
        super().__init__(parent = None, to_move = CHANCE, actions = actions, n = 0)

        self.children = {
            cards: KuhnPlayerMoveGameState(
                self, A, [],  cards, [BET, CHECK], self.n
            ) for cards in self.actions
        }
        # print(self.children)
        self._chance_prob = 1. / len(self.children)

    def is_terminal(self):
        return False

    def inf_set(self):
        return "."

    def chance_prob(self):
        return self._chance_prob

    def sample_one(self):
        return random.choice(list(self.children.values()))

class KuhnPlayerMoveGameState(GameStateBase):

    def __init__(self, parent, to_move, actions_history, cards, actions, n):
        super().__init__(parent = parent, to_move = to_move, actions = actions, n = n)
        # print(parent)
        self.n += 1

        self.actions_history = actions_history
        self.cards = cards
        self.children = {
            a : KuhnPlayerMoveGameState(
                self,
                -to_move,
                self.actions_history + [a],
                cards,
                self.__get_actions_in_next_round(a),
                self.n
            ) for a in self.actions
        }
        # print(self.children)

        public_card = self.cards[0] if self.to_move == A else self.cards[1]
        self._information_set = ".{0}.{1}".format(public_card, ".".join(self.actions_history))
        print('level', self.n)
        # print('cards', self.cards, 'public_card', public_card)
        print('inf_set', self._information_set)

    def __get_actions_in_next_round(self, a):
        if len(self.actions_history) == 0 and a == BET:
            return [FOLD, CALL]
        elif len(self.actions_history) == 0 and a == CHECK:
            return [BET, CHECK]
        elif self.actions_history[-1] == CHECK and a == BET:
            return [CALL, FOLD]
        elif a == CALL or a == FOLD or (self.actions_history[-1] == CHECK and a == CHECK):
            return []

    def inf_set(self):
        return self._information_set

    def is_terminal(self):
        return self.actions == []

    def evaluation(self):
        if self.is_terminal() == False:
            raise RuntimeError("trying to evaluate non-terminal node")

        if self.actions_history[-1] == CHECK and self.actions_history[-2] == CHECK:
            return RESULTS_MAP[self.cards] * 1

        if self.actions_history[-2] == BET and self.actions_history[-1] == CALL:
            return RESULTS_MAP[self.cards] * 2

        if self.actions_history[-2] == BET and self.actions_history[-1] == FOLD:
            return self.to_move * 1
