"""
人工势场法解决一定空域内20架飞机的解脱
飞行速度：https://wenda.so.com/q/1464487169720970
"""

import numpy as np
import imageio
import cv2
import math
import random
from datetime import datetime

from positional import *
from objects import *
from pyproj import Transformer


# def tCrash(position1, position2):
#     print("GG")
#     return 0


# 主函数
if __name__ == '__main__':

    list5=[]
    list10=[]
    list15=[]
    list20 = []
    # 以沈阳机场作为参考点，20km*20km空域
    lat = 41.635475
    lon = 123.49275

    # 定义网格（环境） 20km*20km  速度：200m/s   100格*100格
    # 数据处理：20km * 20km空域 速度200m/s则：格子数：20_000/200 = 100  （定义格子大小为 10）
    world_size = (800, 800)
    # 用白色初始化空白画布
    image = np.ones((world_size[1], world_size[0], 3), dtype=np.uint8) * 255

    # 绿色：智能体  深蓝色：目的点
    # random.randint(a,b)：用于生成一个指定范围内的整数。其中参数a是下限，参数b是上限，生成的随机数n：a<=n<=b
    # 定义智能体：
    agents = []
    for index in range(20):
        agents.append(Agent(Position(random.randint(1,79)*10,random.randint(1,79)*10), sigma=3 ,scan_radius=1, possible_moves=8))

    for agent in agents:
        agent.drawCircleStart(image)

    # 目的点：
    goals =[]
    for index in range(20):
        goals.append(Goal(Position(0,random.randint(0,79)*10), sigma=math.sqrt(world_size[0] ** 2 + world_size[1] ** 2)))
        goals.append(Goal(Position(random.randint(0,79)*10,0), sigma=math.sqrt(world_size[0] ** 2 + world_size[1] ** 2)))
        goals.append(Goal(Position(790,random.randint(0,79)*10), sigma=math.sqrt(world_size[0] ** 2 + world_size[1] ** 2)))
        goals.append(Goal(Position(random.randint(0,79)*10,790), sigma=math.sqrt(world_size[0] ** 2 + world_size[1] ** 2)))
    for goal in goals:
        goal.drawCircle(image)


    # 显示初始画面并等待开始
    cv2.imshow('CDR', image)
    cv2.waitKey(1)
    # 价值权重
    cost_weight = 20
    # 价值
    cost = 0
    # 计数
    count = 0
    # 方向
    direction = 1
    # picture = 0

    # 定义没有达到目的点的飞机数量
    aircrafts = len(agents)
    # 记录到达目的点的飞机坐标
    arrlist = []

    while aircrafts != 0:
        for index1 in range(aircrafts):
            # 10
            if (Position.calculate_distance(agents[index1].position, goals[index1].position) <= 5):
                # 距离小于10时 证明达到目的地 将该智能体与目标点去除
                print("已有一架飞行器安全飞出空域！")
                # 记录飞机列表坐标
                arrlist.append(index1)

        # 将已到达目的的飞机删掉   注意：先清理坐标大的飞机 不然列表删除后会报错（从小到大处理会报错  应该是从大到小！！！！！）
        # 将序列倒序
        arrlist.reverse()
        for k in arrlist:
            del agents[k]
            del goals[k]
            aircrafts = aircrafts - 1
        # 重新赋予空值
        arrlist = []


        # 计算智能体与目标点的距离：若没到到目标点 则继续进行下一步移动
        for index2 in range(aircrafts):
            # 访问列表
            visited_list = []
            if (Position.calculate_distance(agents[index2].position, goals[index2].position) > 5):
                possible_moves = agents[index2].get_possible_moves()
                min_value = math.inf
                best_move = possible_moves[0]  # 将智能体下一步可能走到的位置的列表中的第一个可能性作为最佳移动（最佳移动的初始化）  8个位置
                # 用最小值查找移动
                for move in possible_moves:
                    # 移动价值为与目的点的引力值
                    move_value = goals[index2].get_attraction_force(move)
                    for i in range(len(agents)):
                        if (i != index2) and (Position.calculate_distance(agents[index2].position, agents[i].position)<=100):
                            # 计算斥力
                            # move_value += agents[i].get_repulsion_force_pre(move)

                             move_value += agents[i].get_repulsion_force(move)

                    # # 若果移动的坐标点在访问列表中 ：print：测试   且   移动价值加一
                    # if len(visited_list)>=1:
                    #     if PtoXY(move) in visited_list[len(visited_list)-1:]:
                    #         move_value += 1
                    #
                    # for j in range(aircrafts):
                    #     for k in range(j+1, aircrafts):
                    #         if Position.calculate_distance(agents[j].position, agents[k].position) == 0:
                    #             move_value += 1


                    # 更新最小价值且和赋值给最佳移动位置
                    if move_value < min_value:
                        min_value = move_value
                        best_move = move
                        # 将这位置加入访问列表
                        visited_list.append(PtoXY(move))


            # 将最佳移动设置为代理的下一个位置
            agents[index2].position = best_move

            '''start'''
            # lat = 41.635475
            # lon = 123.49275
            # transformer = Transformer.from_crs("epsg:4326", "epsg:32649")
            # x, y = transformer.transform(lat, lon)
            #
            # x = x+PtoXY1(best_move)[0] * 25
            # y = y+PtoXY1(best_move)[1] * 25
            #
            #
            # transformer = Transformer.from_crs("epsg:32649", "epsg:4326")
            # lat, lon = transformer.transform(x, y)
            # if(index2 == 5):
            #     list5.append("$AP,"+str(index2)+","+ str(lon)+','+ str(lat)+','+str(datetime.now())[:-7])
            # if (index2 == 10):
            #     list10.append("$AP," + str(index2) + "," + str(lon) + ',' + str(lat) + ',' + str(datetime.now())[:-7])
            # if (index2 == 15):
            #     list15.append("$AP," + str(index2) + "," + str(lon) + ',' + str(lat) + ',' + str(datetime.now())[:-7])
            # if (index2 == 19):
            #     list20.append("$AP," + str(index2+1) + "," + str(lon) + ',' + str(lat) + ',' + str(datetime.now())[:-7])
            #
            # print("$AP,"+str(index2)+","+ str(lon)+','+ str(lat)+','+str(datetime.now())[:-7] )
            # if len(list20)>15:
            #     print("======================")
            #     for index in range(0, 10):
            #         print(list5[index])
            #
            #     print("=========================")
            #     for index in range(0, 10):
            #         print(list10[index])
            #     print("=========================")
            #     for index in range(0, 10):
            #         print(list15[index])
            #     print("=========================")
            #     for index in range(0, 10):
            #         print(list20[index])
            '''end'''


        '''
        因为没有在每次迭代时清理初始帧
        所以不用重新绘制
        '''
        for goal in goals:
            goal.drawCircle(image)
        for index3 in range(aircrafts):
            agents[index3].drawCircle(image)
        for j in range(aircrafts):
            for k in range(j+1, aircrafts):
                if Position.calculate_distance(agents[j].position, agents[k].position) == 0:
                    print("GGG")
        # flag_crash = False
        # for j in range(aircrafts):
        #     if (j != index3):
        #         if agents[index3].position.calculate_distance(agents[j].position) <= 3:
        #             flag_crash = True
        #
        #     if (flag_crash):
        #         break



        # 显示更新帧
        cv2.imshow('CDR', image)
        # # 保存每一帧 用于合成视频
        # path = './result/test'+str(picture)+'.jpg'
        # cv2.imwrite(path,image,[int(cv2.IMWRITE_JPEG_QUALITY),100])
        # picture = picture + 1


        # ESC的对应ASCII码值为27
        k = cv2.waitKey(1)
        if k == 27:
            break

    print("执行完毕")
    #cv2.imwrite('CDR.png', image)


    # 保持最后一帧
    cv2.waitKey(0)



