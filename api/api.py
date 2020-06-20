from flask import Flask

app = Flask(__name__)


@app.route('/koms')
def koms():
    return {'miles': 7, 'lee':16}
