from flask import Flask, render_template, request, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit
from brainflow.board_shim import BrainFlowError
from enviroment import boards_properties, connection_element_names
from boards import MainBoard
from time import sleep # TODO REMOVEE

app = Flask(__name__)

#https://github.com/gothinkster/flask-realworld-example-app

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.debug = True

socketio = SocketIO(app)
BOARD = MainBoard()
Session(app)

@app.context_processor
def variables_setup():
    return {"boards_properties": boards_properties, "connection_element_names" : connection_element_names}

@app.route("/connect", methods=["GET", "POST"])
def connect():
    alert = None
    # check connection - if not connected render : connect else dashboard
    if request.method == "POST":
        board_id, log_level, params = BOARD.extract_params(request)
        if board_id:
            try:
                BOARD.set_board(board_id, params)
                BOARD.board.set_log_level(log_level)
                BOARD.connect()
            except BrainFlowError as e:
                alert = e
        else:
            alert = "Board ID not specified"
    if BOARD.connected:
        return redirect(url_for("dashboard"))
    return render_template("connect.html", status=BOARD.status_message, message=alert)

@app.route("/dashboard")
def dashboard():
    if BOARD.connected:
        return render_template("dashboard.html")
    return redirect(url_for("connect"))


@app.route("/disconnect", methods=["POST"])
def disconnect():
    BOARD.disconnect()
    return redirect(url_for("connect"))

@socketio.on("start-stream")
def data_stream_control(data):
    if data["action"] == "start":
        BOARD.board.start_stream()
        # TODO: separate files !! - change strucure !!!
        while True:
            data = BOARD.get_json_data()
            if data:
                emit("return data", data)
            sleep(BOARD.emit_delay)
    else:
        BOARD.board.stop_stream()


if __name__ == "__main__":
    app.run()