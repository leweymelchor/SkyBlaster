from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return os.system('main.py')


if __name__ == '__main__':
    app.run()
