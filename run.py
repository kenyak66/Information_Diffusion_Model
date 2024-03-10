from pyibl import Agent
import random
import mesa

from infodif import PlayerAgent, Item 

grid_size = 5
number_of_agents = 3
symbols = ["blank", "square", "pall", "trape", "prizm", "tri"]
directions = ["up", "down", "left", "right"]
agents = []

# エージェントの生成と配置
for i in range(number_of_agents):
    name = "agent" + str(i)
    initial_coordinate = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
    agents.append(PlayerAgent(attributes=["direction", "slot1" "slot2", "slot3"], name=name, coordinate=initial_coordinate))

# グリッドの作成
grid = mesa.space.MultiGrid(grid_size, grid_size, True)

# エージェントの配置
for agent in agents:
    x, y = agent.coordinate
    grid.place_agent(agent, (x, y))


# ステップの実行
for agent in agents:
    slot1 = agent.choose(symbols)
    slot2 = agent.choose(symbols)
    slot3 = agent.choose(symbols)
    agent.attributes["slot1"] = slot1
    agent.attributes["slot2"] = slot2
    agent.attributes["slot3"] = slot3

for agent in agents:
    direction = agent.choose(directions)
    agent.attributes["direction"] = direction
    x, y = agent.coordinate
    if direction == "up":
        new_coordinate = (x, y + 1)
    elif direction == "down":
        new_coordinate = (x, y - 1)
    elif direction == "left":
        new_coordinate = (x - 1, y)
    elif direction == "right":
        new_coordinate = (x + 1, y)

    if grid.is_cell_empty(new_coordinate):
        agent.coordinate = new_coordinate
        grid.move_agent(agent, new_coordinate)
