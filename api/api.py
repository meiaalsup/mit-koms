from flask import Flask

app = Flask(__name__)


@app.route('/miles')
def miles():
    return {'miles': 7}


@app.route('/lee')
def lee():
    return {'lee': 16}

