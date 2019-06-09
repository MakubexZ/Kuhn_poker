from common.constants import CARDS_DEALINGS
from games.kuhn import KuhnRootChanceGameState
from games.algorithms import ChanceSamplingCFR, VanillaCFR

root = KuhnRootChanceGameState(CARDS_DEALINGS)

chance_sampling_cfr = ChanceSamplingCFR(root)
for _ in range(100):
    chance_sampling_cfr.run(iterations = 10)
    chance_sampling_cfr.compute_nash_equilibrium()


vanilla_cfr = VanillaCFR(root)
for _ in range(100):
    vanilla_cfr.run(iterations = 5)
    vanilla_cfr.compute_nash_equilibrium()
