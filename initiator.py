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


def fun_timer():
    global timer
    rand = random.randint(0, 8)
    label[0] = rand
    count[0] += 1
    print(str(count[0]) + ': ' + labelMap[rand])
    if count[0] < MAX_COUNT[0]:
        timer = threading.Timer(random.randint(3, 10), fun_timer)
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

label = [4]
labelMap = ['LEFT UP', 'CENTER UP', 'RIGHT UP', 'LEFT CENTER', 'CENTER CENTER', 'RIGHT CENTER', 'LEFT DOWN', 'CENTER DOWN', 'RIGHT DOWN']
count = [1]
MAX_COUNT = [30]
print('--------------------------------')
print('READY? GO!')
print('--------------------------------')
print('1: CENTER CENTER')
timer = threading.Timer(random.randint(3, 10), fun_timer)
timer.start()


# 处理数据

data = []
labels = []

label_stand = [0]
label_run = [0]
dataArray = [[]]


@app.route('/', methods=['POST'])
def post():
    json = request.get_json()
    if label[0] == 0:
        label_stand[0] += 1
    else:
        label_run[0] += 1
    array = []
    for point in json['keyPoints'].values():
        array.append([point['score'], point['position']
                      ['x'] / 300, point['position']['y'] / 300])
    dataArray[0].append(array)

    # 当数据达到24时:
    if len(dataArray[0]) >= 24:
        if label_stand[0] >= label_run[0]:
            labels.append(0)
        else:
            labels.append(1)
        data.append(dataArray[0])
        # 清理
        label_stand[0] = 0
        label_run[0] = 0
        dataArray[0] = []

    return 'Success'


def train():
    index = np.arange(len(data))
    np.random.shuffle(index)
    train_images = np.array(data)[index]
    train_labels = np.array(labels)[index]
    np.savez('trainData.npz', train_images=train_images, train_labels=train_labels)
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(24, 17, 3)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(9)
    ])
    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
    model.fit(train_images, train_labels, epochs=20)
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    probability_model.save('newmodel.h5')
    model.save('newpremodel.h5')


if __name__ == "__main__":
    app.run(debug=False)
    # $env:FLASK_APP = "initiator.py"
    # flask run --host=0.0.0.0
