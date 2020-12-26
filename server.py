from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    json = request.get_json()
    print(json['time'])
    with open('data.json', 'a', encoding='utf-8') as f:
        f.write(str(json) + '\n')  # dict to str
    return 'Success'
    
def load():
    with open('data.json', 'r', encoding='utf-8') as f:
        dict = eval(f.readline().strip())  # eval
        print(dict)

if __name__ == "__main__":
    app.run(debug=False)
    # $env:FLASK_APP = "server.py"
    # flask run --host=0.0.0.0
