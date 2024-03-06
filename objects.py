import math
import cv2
from positional import Position
import random


# 智能体类 用于描述智能体属性
class Agent:
    """
    position:位置，智能体在地图上的位置
    scan_radius:int，可选，智能体的步长，默认为1
    possible_moves:int，可选，代理周围生成的点数，默认为6
    draw_radius:int，可选，可视化半径，默认为5
    draw_color:元组，可选 默认情况下用于可视化的颜色（255,0,0）
    """
    # σ越大，数据分布越分散，σ越小，数据分布越集中
    def __init__(self, position, scan_radius=1, possible_moves=20, draw_radius=10, draw_color=(46, 139, 87),mu=1, sigma=10,direction=1):
        # 属性
        self.position = position
        self._scan_radius = scan_radius
        self._possible_moves = possible_moves
        ########
        self.lastposition = position
        self._mu = mu
        self.direction = direction
        self._sigma = sigma

        # 感知属性
        self._draw_radius = draw_radius
        self._draw_color = draw_color

    def draw(self, image):
        # cv2.circle(image, (int(self.position.x), int(self.position.y)), self._draw_radius, self._draw_color, -1)  # Fill
        x1 = int(self.position.x)  # 类型强转
        y1 = int(self.position.y)
        cv2.rectangle(image, (x1, y1), (x1 + self._draw_radius, y1 + self._draw_radius), self._draw_color, -1)

    def drawCircleStart(self, image):
        # cv2.circle(image, (int(self.position.x), int(self.position.y)), self._draw_radius, self._draw_color, -1)  # Fill
        x1 = int(self.position.x)  # 类型强转
        y1 = int(self.position.y)
        cv2.rectangle(image, (x1, y1), (x1 + 5, y1 + 5),(0, 0, 128), -1)
    def drawCircle(self, image):
        # cv2.circle(image, (int(self.position.x), int(self.position.y)), self._draw_radius, self._draw_color, -1)  # Fill
        x1 = int(self.position.x)  # 类型强转
        y1 = int(self.position.y)
        cv2.rectangle(image, (x1, y1), (x1+2 , y1+2 ), self._draw_color, -1)



    def get_possible_moves(self):
        """
        求解智能体下一步可能走的、周围的点（下一位置的可能性）
        返回值：智能体下一阶段可能走到的周围的点（列表）
        """
        angle_increment = (2 * math.pi) / self._possible_moves  # 2pi/n
        angle = -angle_increment  # Going one step negative to start from zero  从零开始负一步
        possible_moves_list = []
        for _ in range(self._possible_moves):
            # 角度从0开始
            angle += angle_increment
            possible_moves_list.append(Position(self._scan_radius * math.cos(angle) + self.position.x,
                                                self._scan_radius * math.sin(angle) + self.position.y))
            # possible_moves_list.append(Position(self.position.x))
        return possible_moves_list


    def get_repulsion_force_pre(self, position):
        print('position', self.position.x)
        print('lastposition ', self.lastposition.x)

        predict_position = self.position + self.position - self.lastposition
        print('predictposition ', predict_position.x)
        print('------------------------------------')

        position_list_cal = [predict_position, Position(predict_position.x + 10, predict_position.y),
                             Position(predict_position.x, predict_position.y + 10),
                             Position(predict_position.x + 10, predict_position.y + 10)]
        dist_value = 0
        for Ever_position in position_list_cal:
            dist_value += (1 / (self._sigma * math.sqrt(2 * math.pi))) * math.exp(
                -(Position.calculate_distance_squared(Ever_position, position) / (2 * self._sigma * self._sigma)))
        return dist_value

    def get_repulsion_force(self, position):
        dist_value = (1 / (self._sigma * math.sqrt(2 * math.pi))) * math.exp(
            -(Position.calculate_distance_squared(self.position, position) / (2 * self._sigma * self._sigma)))
        return dist_value



# 目的点
class Goal:
    """
    https://qiao.github.io/PathFinding.js/visual/
    创建目标对象
    参数
    ----------
    position:位置 目标在世界上的地位
    mu:int，可选 分布峰值，默认为1
    sigma:int，可选 分布范围，默认情况下1
    draw_radius:int，可选 可视化半径，默认为5
    draw_color:元组，可选访问https://qiao.github.io/PathFinding.js/visual/   默认情况下，用于可视化的颜色（0255,0）
    """

    def __init__(self, position, mu=1, sigma=1, draw_radius=10, draw_color=(128, 0, 0)):
        # 属性
        self.position = position
        self._mu = mu
        self._sigma = sigma

        # 感知属性
        self._draw_radius = draw_radius
        self._draw_color = draw_color

    def draw(self, image):
        x1 = int(self.position.x)
        y1 = int(self.position.y)
        cv2.rectangle(image, (x1, y1), (x1 + self._draw_radius, y1 + self._draw_radius), self._draw_color, -1)


    def drawCircle(self, image):
        # cv2.circle(image, (int(self.position.x), int(self.position.y)), self._draw_radius, self._draw_color, -1)  # Fill
        x1 = int(self.position.x)  # 类型强转
        y1 = int(self.position.y)
        cv2.rectangle(image, (x1, y1), (x1 + 5, y1 + 5), self._draw_color, -1)
    # 计算引力
    def get_attraction_force(self, position):
        # 引力方程
        dist_value = -(1 / (self._sigma * math.sqrt(2 * math.pi))) * math.exp(
            -(Position.calculate_distance_squared(self.position, position) / (2 * self._sigma * self._sigma)))
        return dist_value
