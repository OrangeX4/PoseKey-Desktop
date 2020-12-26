from flask import Flask, request
from tensorflow import keras
app = Flask(__name__)

@app.route('/', methods=['POST'])
def post():
    probability_model = keras.models.load_model('model.h5')
    # predictions = probability_model.predict(test_images)
    json = request.get_json()
    print(json['time'])
    with open('data.json', 'a', encoding='utf-8') as f:
        f.write(str(json) + '\n')  # dict to str
    return 'Success'

if __name__ == "__main__":
    app.run(debug=False)
    # $env:FLASK_APP = "server.py"
    # flask run --host=0.0.0.0
    