import random

HomexG = [0.21,0.66,0.1,0.14,0.01]
AwayxG = [0.04,0.06,0.01,0.04,0.06,0.12,0.01,0.06]

if random.random() <= 0.21:
    print("GOAL!")

else:
    print("oh missed!")

Goals = 0

for j in range(0, 1000):
    if random.random() <=0.1:
        Goals +=1
print(Goals)
