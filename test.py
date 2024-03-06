import random

list=[0,0,0,0,0,0,0,0,0,0,0,0]
for i in range(0,1000_000):
    a = random.randint(1, 12)
    if(a==1):
        list[0]=list[0]+1
    if (a == 2):
        list[1] = list[1] + 1
    if (a == 3):
        list[2] = list[2] + 1
    if (a == 4):
        list[3] = list[3]+1
    if (a == 5):
        list[4] = list[4]+1
    if (a == 6):
        list[5] = list[5]+1
    if (a == 7):
        list[6] = list[6]+1
    if (a == 8):
        list[7] = list[7]+1
    if (a == 9):
        list[8] = list[8]+1
    if (a == 10):
        list[9] = list[9]+1
    if (a == 11):
        list[10] = list[10]+1
    if (a == 12):
        list[11] = list[11]+1
for index in range(len(list)):
    list[index] = list[index]/1000_000
print(list)