from flask import Flask

app = Flask(__name__)


@app.route('/ass')
def hello():
    return 'Hello World!'
