from pyibl import Agent as PyIBLAgent
import random
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from infodif_pair import PlayerAgent

symbols = ["blank", "square", "pall", "trape", "prizm", "tri"] 
messages = []

class InformationDiffusionModel(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # エージェントの生成と配置
        for i in range(2):  # エージェントを2体のみ生成する
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            a = PlayerAgent(i, attributes=("slot1", "slot2", "slot3"), default_utility=10.0, coordinate=[x, y])
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)

    def step(self):
        self.schedule.step()

# モデルの作成と実行
model = InformationDiffusionModel(10, 10)
for _ in range(10):
    model.step()

# エージェントの位置の確認
for agent in model.schedule.agents:
    print("Agent", agent.unique_id, "at", agent.coordinate)
