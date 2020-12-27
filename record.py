from flask import Flask, request
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
    if label[0] == 0:
        label[0] = 1
        count[0] += 1
        print('RUN')
    else:
        label[0] = 0
        count[0] += 1
        print('STAND')
    if count[0] < MAX_COUNT[0]:
        timer = threading.Timer(random.randint(3, 10), fun_timer)
        timer.start()
    else:
        print('STOP')


# 初始化定义
label = [0]
count = [1]
MAX_COUNT = [10]
print('STAND')
timer = threading.Timer(random.randint(3, 10), fun_timer)
timer.start()



@app.route('/', methods=['POST'])
def post():
    json = request.get_json()
    json['label'] = label[0]
    with open('temp.json', 'a', encoding='utf-8') as f:
        f.write(str(json) + '\n')  # dict to str
    return 'Success'


if __name__ == "__main__":
    app.run(debug=False)
    # $env:FLASK_APP = "record.py"
    # flask run --host=0.0.0.0
