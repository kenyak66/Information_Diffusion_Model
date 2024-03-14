from pyibl import Agent
import numpy as np
import random
import mesa

grid_size = 3
number_of_agents = 2
number_of_items = 1
symbols = ["blank", "square", "pall", "trape", "prizm", "tri"] # 図形の要素はベクトルと類似度で表現したい
directions = ["up", "down", "left", "right"]
attributes = ["direction", "slot1", "slot2", "slot3"]
agents = []

class PlayerAgent(Agent):
    def __init__(self, attributes=(), name=None, noise=0.25, decay=0.5, temperature=None, mismatch_penalty=None, optimized_learning=False, default_utility=10.0, default_utility_populates=False, fixed_noise=False, location=(0, 0)):
        super().__init__(attributes, name, noise, decay, temperature, mismatch_penalty, optimized_learning, default_utility, default_utility_populates, fixed_noise)
        self.location = location  # エージェントの座標
        self.neighbors = []  # 隣接するマスの情報
        self.point = 0  # エージェントの得点
        self.slot1 = "blank"
        self.slot2 = "blank"
        self.slot3 = "blank"
        self.messages = [] # 他のエージェントのメッセージ

    # 隣接するマスの情報を設定
    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
    
    # 隣接するマスの情報を取得
    def get_neighbors(self):
        return self.neighbors
    
    # 図形を選択
    def choose_message(self):
        slot1 = self.choose(symbols)
        slot2 = self.choose(symbols)
        slot3 = self.choose(symbols)
        self.attributes["slot1"] = slot1
        self.attributes["slot2"] = slot2
        self.attributes["slot3"] = slot3
    

#エージェントを一人作成し、メッセージを送信する
agent = PlayerAgent(attributes=["direction", "slot1", "slot2", "slot3"], name="agent0", location=(0, 0))
#エージェントの要素を表示
print(agent.attributes)
agent.choose_message()
agent.send_message()
