from flask import Flask, request
from flask import g
import threading
import random
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)


# def fun_timer():
#     global timer
#     if label[0] == 0:
#         label[0] = 1
#         print('RUN')
#     else:
#         label[0] = 0
#         print('STAND')
#     timer = threading.Timer(random.randint(3, 10), fun_timer)
#     timer.start()


# STAND
# label = [0]
# print('STAND')
# timer = threading.Timer(random.randint(3, 10), fun_timer)
# timer.start()


@app.route('/', methods=['POST'])
def post():
    json = request.get_json()
    json['label'] = 0
    with open('autodata.json', 'a', encoding='utf-8') as f:
        f.write(str(json) + '\n')  # dict to str
    return 'Success'


if __name__ == "__main__":
    app.run(debug=False)
    # $env:FLASK_APP = "record.py"
    # flask run --host=0.0.0.0
