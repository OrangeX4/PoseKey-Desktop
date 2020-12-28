from flask import Flask, request
import os
import numpy as np
import tensorflow as tf
import threading
import random
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)

# ------------------
# 定时器获取数据


def weightedRandom(weighted):
    r = random.randint(1, sum(weighted))
    c = 0
    for index, w in enumerate(weighted):
        c = c + w
        if c >= r:
            return index


def fun_timer():
    global timer
    # 对于HEAD: 给中间状态增加训练权重
    headRand = weightedRandom([1, 3, 1, 1, 5, 1, 1, 3, 1])
    headLabel[0] = headRand
    # 对于STAND:
    standRand = weightedRandom([2, 1])
    standLabel[0] = standRand
    # count计数, 直到最大的MAX_COUNT就停止
    count[0] += 1
    print(str(count[0]) + ': ' + standLabelMap[standRand] +
          ' ' + headLabelMap[headRand])
    if count[0] < MAX_COUNT[0]:
        timer = threading.Timer(random.randint(5, 10), fun_timer)
        timer.start()
    else:
        print('STOP')
        print('--------------------------------')
        print('We will train the model for you.')
        print('--------------------------------')
        train()
        print('--------------------------------')
        print('Welcome to try the new model!')
        print('--------------------------------')
        os._exit(0)


# 初始化定义

headLabel = [4]
headLabelMap = ['LEFT UP', 'CENTER UP', 'RIGHT UP', 'LEFT CENTER',
                'CENTER CENTER', 'RIGHT CENTER', 'LEFT DOWN', 'CENTER DOWN', 'RIGHT DOWN']
standLabel = [0]
standLabelMap = ['STAND', 'RUN']
count = [1]
MAX_COUNT = [20]
print('--------------------------------')
print('READY? GO!')
print('--------------------------------')
print('1: STAND CENTER CENTER')
timer = threading.Timer(random.randint(3, 10), fun_timer)
timer.start()


# 处理数据
try:
    dataFile = np.load('data.npz')
except:
    data = []
    headLabels = []
    standLabels = []
else:
    data = dataFile['data'].tolist()
    headLabels = dataFile['headLabels'].tolist()
    standLabels = dataFile['standLabels'].tolist()

print(len(data))

headLabelCount = [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
standLabelCount = [[0, 0]]
dataArray = [[]]


def getMaxIndex(array):
    maxValue = max(array)  # 返回最大值
    return array.index(maxValue)


@app.route('/', methods=['POST'])
def post():
    json = request.get_json()
    headLabelCount[0][headLabel[0]] += 1
    standLabelCount[0][standLabel[0]] += 1
    array = []
    for point in json['keyPoints'].values():
        array.append([point['score'], point['position']
                      ['x'] / 300, point['position']['y'] / 300])
    dataArray[0].append(array)

    # 当数据达到24时:
    if len(dataArray[0]) >= 24:
        headLabels.append(getMaxIndex(headLabelCount[0]))
        standLabels.append(getMaxIndex(standLabelCount[0]))
        # print('Label: ' + str(getMaxIndex(standLabelCount[0])))
        data.append(dataArray[0])
        # 清理
        headLabelCount[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        standLabelCount[0] = [0, 0]
        dataArray[0] = []

    return 'Success'


def train():
    index = np.arange(len(data))
    np.random.shuffle(index)
    shuffledData = np.array(data)[index]
    shuffledHeadLabels = np.array(headLabels)[index]
    shuffledStandLabels = np.array(standLabels)[index]
    np.savez('data.npz', data=shuffledData,
             headLabels=shuffledHeadLabels, standLabels=shuffledStandLabels)
    headModel = tf.keras.models.load_model('headModel.h5')
    headModel.fit(shuffledData, shuffledHeadLabels, epochs=20)
    headModel.save('headModel.h5')
    standModel = tf.keras.models.load_model('standModel.h5')
    standModel.fit(shuffledData, shuffledStandLabels, epochs=20)
    standModel.save('standModel.h5')


if __name__ == "__main__":
    app.run(debug=False)
    # $env:FLASK_APP = "learner.py"
    # flask run --host=0.0.0.0
