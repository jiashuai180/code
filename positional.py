import math

# 计算两点之间距离
class Position:
    """
    参数：
    x : double
        x坐标
    y : double
        y坐标

    """

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
    # 加
    def __add__(self, other):
        result_x = self.x + other.x
        result_y = self.y + other.y

        return Position(result_x, result_y)
    # 减
    def __sub__(self, other):
        result_x = self.x - other.x
        result_y = self.y - other.y

        return Position(result_x, result_y)

    # 计算距离
    def calculate_distance(self, other):

        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    # General type function
    def calculate_distance_squared(self, other):
        """
        计算当前位置与作为参数传递的位置之间的平方距离
        """

        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

# 转换成坐标形式
def PtoXY(P):
    xy = (P.x, P.y)
    return xy

def PtoXY1(P):
    li = []
    li.append(P.x)
    li.append(P.y)

    return li