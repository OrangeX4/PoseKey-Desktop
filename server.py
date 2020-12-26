from flask import Flask, request
from tensorflow.keras.models import load_model
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
model = load_model('model.h5')
data = []

@app.route('/', methods=['POST'])
def post():
    json = request.get_json()
    array = []
    for point in json['keyPoints'].values():
        array.append([point['score'], point['position']['x'] / 300, point['position']['y'] / 300])
    data.append(array)
    if len(data) == 12:
        predictions = model.predict([data[:12]])
        if predictions[0][0] > 0.5:
            print('STAND')
        else:
            print('RUN')
        data.clear()
    return 'Success'

if __name__ == "__main__":
    app.run(debug=False)
    # $env:FLASK_APP = "server.py"
    # flask run --host=0.0.0.0
    