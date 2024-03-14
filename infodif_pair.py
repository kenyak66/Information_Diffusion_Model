from pyibl import Agent as PyIBLAgent
import random
import matplotlib.pyplot as plt

symbols = ["blank", "square", "pall", "trape", "prizm", "tri"] 
messages = []

class PlayerAgent(PyIBLAgent):
    # エージェントの初期化
    def __init__(self, attributes=(), name=None, noise=0.25, decay=0.5, temperature=None, mismatch_penalty=None, optimized_learning=False, default_utility=10.0, default_utility_populates=False, fixed_noise=False, coordinate=[0, 0]):
        super().__init__(attributes, name, noise, decay, temperature, mismatch_penalty, optimized_learning, default_utility, default_utility_populates, fixed_noise)
        self.coordinate = coordinate # エージェントの座標
        self.received_message = {"slot1": "blank", "slot2": "blank", "slot3": "blank"} # 他のエージェントから受け取ったメッセージ
        self.neighbors = [] # 隣接するマスの情報
    
    # メッセージを選択して送信(IBLのchooseメソッドを利用)
    def send_message(self):
        return self.choose(messages)
    
    # 他のエージェントからのメッセージを受け取る
    def get_message(self, received_message):
        self.received_message = received_message
    
    # エージェントの移動
    def move(self):
        message = self.received_message
        if message["slot1"] == message["slot2"] == message["slot3"]:# 3つのスロットが同じ場合y座標を1増やす
            self.coordinate = (self.coordinate[0], self.coordinate[1] + 1)
        elif message["slot1"] == message["slot3"]:# 2つのスロット(slot1, slot3)が同じ場合y座標を1減らす
            self.coordinate = (self.coordinate[0], self.coordinate[1] - 1)
        elif message["slot1"] == message["slot2"]:# 2つのスロット(slot1, slot2)が同じ場合x座標を1減らす
            self.coordinate = (self.coordinate[0] - 1, self.coordinate[1])
        elif message["slot2"] == message["slot3"]:# 2つのスロット(slot2, slot3)が同じ場合x座標を1増やす
            self.coordinate = (self.coordinate[0] + 1, self.coordinate[1])
        else:# それ以外の場合ランダムに移動
            if random.random() < 0.5:
                self.coordinate = (self.coordinate[0] + random.choice([-1, 1]), self.coordinate[1])
            else:
                self.coordinate = (self.coordinate[0], self.coordinate[1] + random.choice([-1, 1]))
    
    # エージェントの報酬を計算
    def calc_outcome(self, other):
        distance = abs(self.coordinate[0] - other.coordinate[0]) + abs(self.coordinate[1] - other.coordinate[1])
        outcome = 1/(distance + 1) # マンハッタン距離の逆数を報酬としている (近い方が高い報酬を得る)
        self.respond(outcome)


# 5つの図形(+空白)からなる全ての組み合わせを生成
def create_messages(symbols):
    for symbol1 in symbols:
        for symbol2 in symbols:
            for symbol3 in symbols:
                message = {"slot1": symbol1, "slot2": symbol2, "slot3": symbol3} # 3つのスロットに図形を格納
                messages.append(message)

# 実行
def run():
    # メッセージの生成
    create_messages(symbols)  

    # エージェントの座標を記録するリスト
    agent1_coordinates = []
    agent2_coordinates = []

    # 二つのエージェントを作成
    agent1 = PlayerAgent(attributes=("slot1", "slot2", "slot3"), default_utility=10.0, coordinate=[0, 0])
    agent2 = PlayerAgent(attributes=("slot1", "slot2", "slot3"), default_utility=10.0, coordinate=[3, 3])

    # 100ターン分のシミュレーションを実行
    for _ in range(100):  
        # エージェントの座標を記録
        agent1_coordinates.append(agent1.coordinate)
        agent2_coordinates.append(agent2.coordinate)

        # エージェントがメッセージを選択して交換
        message1 = agent1.send_message()
        message2 = agent2.send_message()
        agent1.get_message(message2)
        agent2.get_message(message1)

        # エージェントが移動
        agent1.move()
        agent2.move()

        # エージェントの報酬を計算
        agent1.calc_outcome(agent2)
        agent2.calc_outcome(agent1)

    agent1.instances()
    agent2.instances()

    # グラフの描画
    plt.plot([coord[0] for coord in agent1_coordinates], [coord[1] for coord in agent1_coordinates], label='Agent 1')
    plt.plot([coord[0] for coord in agent2_coordinates], [coord[1] for coord in agent2_coordinates], label='Agent 2')
    plt.plot(agent1_coordinates[0][0], agent1_coordinates[0][1], 'o', color='blue')  # Agent 1 の初期位置を○でマーク
    plt.plot(agent2_coordinates[0][0], agent2_coordinates[0][1], 'o', color='orange')  # Agent 2 の初期位置を○でマーク
    plt.plot(agent1_coordinates[-1][0], agent1_coordinates[-1][1], '*', color='blue')  # Agent 1 の最終位置を星でマーク
    plt.plot(agent2_coordinates[-1][0], agent2_coordinates[-1][1], '*', color='orange')  # Agent 2 の最終位置を星でマーク
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title('Agent Coordinates Over Time')
    plt.legend()
    plt.show()

run()

