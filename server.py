from flask import Flask, request
from tensorflow.keras.models import load_model
import tensorflow as tf
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
standModel = tf.keras.Sequential([load_model('standModel.h5'), tf.keras.layers.Softmax()])
headModel = tf.keras.Sequential([load_model('headModel.h5'), tf.keras.layers.Softmax()])
data = []
labelMap = ['LEFT UP', 'CENTER UP', 'RIGHT UP', 'LEFT CENTER', 'CENTER CENTER', 'RIGHT CENTER', 'LEFT DOWN', 'CENTER DOWN', 'RIGHT DOWN']
print('STAND')


def getMaxIndex(array):
    array = array.tolist()
    maxValue = max(array)  # 返回最大值
    return array.index(maxValue)


@app.route('/', methods=['POST'])
def post():
    json = request.get_json()
    array = []
    for point in json['keyPoints'].values():
        array.append([point['score'], point['position']
                      ['x'] / 300, point['position']['y'] / 300])
    data.append(array)
    if len(data) == 24:
        standPredictions = standModel.predict([data[:24]])
        headPredictions = headModel.predict([data[:24]])
        # print(predictions[0])
        if standPredictions[0][0] > 0.5:
            print('STAND')
        else:
            print('RUN')
        print(labelMap[getMaxIndex(headPredictions[0])])
        data.clear()
    return 'Success'


if __name__ == "__main__":
    app.run(debug=False)
    # $env:FLASK_APP = "server.py"
    # flask run --host=0.0.0.0
