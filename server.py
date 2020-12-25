from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
# from os import path

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + path.join(app.root_path, 'data.db')
# db = SQLAlchemy(app)


@app.route('/', methods=['POST'])
def hello_world():
    json = request.get_json()
    print(json)
    return 'Success'


if __name__ == "__main__":
    app.run(debug=False)
    # $env:FLASK_APP = "server.py"
    # flask run --host=0.0.0.0
