from common.constants import CARDS_DEALINGS
from games.kuhn import KuhnRootChanceGameState
from games.algorithms import ChanceSamplingCFR, VanillaCFR
import matplotlib.pyplot as plt
import numpy as np


root = KuhnRootChanceGameState(CARDS_DEALINGS)


print('Chance_sampling')
chance_sampling_cfr = ChanceSamplingCFR(root)
X1 = []
Y1 = []
X2 = []
Y2 = []
for i in range(80):
    X1.append(i*10)
    chance_sampling_cfr.run(iterations = 10)
    chance_sampling_cfr.compute_nash_equilibrium()
    value1 = chance_sampling_cfr.value_of_the_game()
    Y1.append(value1)

print('Vanilla')
vanilla_cfr = VanillaCFR(root)
for j in range(80):
    X2.append(j * 10)
    vanilla_cfr.run(iterations = 5)
    vanilla_cfr.compute_nash_equilibrium()
    value2 = vanilla_cfr.value_of_the_game()
    Y2.append(value2)

plt.figure()
plt.plot(X1, Y1, label = 'Chance_sampling')
plt.plot(X2, Y2, color = 'red', label = 'Vanilla')
plt.xlabel('Iterations')
plt.ylabel('Value of Player1')
plt.legend(loc='upper right')
plt.show()
