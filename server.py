from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    json = request.get_json()
    for key, keyPoint in json['keyPoints'].items():
        print('{}: {} {}'.format(
            key, keyPoint['position']['x'], keyPoint['position']['y']))
    return 'Success!'


if __name__ == "__main__":
    app.run(debug=False)
    # $env:FLASK_APP = "server.py"
    # flask run --host=0.0.0.0
