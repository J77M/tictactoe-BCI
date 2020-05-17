from flask import Flask
from flask_socketio import SocketIO
from tttbci.board import MainBoard

app = Flask(__name__)
socketio = SocketIO(app)
DEVICE = MainBoard()

import tttbci.views