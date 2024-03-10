from pyibl import Agent
import numpy as np
import random
import mesa

class PlayerAgent(Agent):
    def __init__(self, attributes=[], name=None, noise=0.25, decay=0.5, temperature=None, mismatch_penalty=None, optimized_learning=False, default_utility=None, default_utility_populates=False, fixed_noise=False, location=(0, 0)):
        super().__init__(attributes, name, noise, decay, temperature, mismatch_penalty, optimized_learning, default_utility, default_utility_populates, fixed_noise)
        self.location = location  # エージェントの座標を追加
        self.neighbors = []  # 隣接するマスの情報を追加

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def get_neighbors(self):
        return self.neighbors


class Item:
    def __init__(self, location):
        self.location = location