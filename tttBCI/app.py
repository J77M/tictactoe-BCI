from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BrainFlowError
from brainflow.exit_codes import BrainflowExitCodes
from enviroment import boards_properties
app = Flask(__name__)

#https://github.com/gothinkster/flask-realworld-example-app

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.debug = True

Session(app)

@app.context_processor
def get_boards_properties():
    return boards_properties

@app.route("/connect", methods=["GET", "POST"])
def connect():
    alert = None
    if session.get("status") is None:
        session["status"] = "not connected"
    # check connection - if not connected render : connect else dashboard
    if request.method == "POST":
        board_id = request.form.get('board_id')
        if board_id:
            # move this shit elsewhere
            params = BrainFlowInputParams()
            params.ip_port = 0
            params.serial_port = request.form.getlist('serial_port')[-1]
            params.mac_address = request.form.getlist('mac_address')[-1]
            params.other_info = '' #TODO
            params.ip_address = '' #TODO
            params.ip_protocol = int(request.form.get("ip_protocol_type"))
            params.timeout = int(request.form.get("timeout"))
            if int(request.form.get("log_level")) != 6:
                BoardShim.enable_dev_board_logger()
            else:
                BoardShim.disable_board_logger()
            try:
                global board
                board = BoardShim(int(request.form.get('board_id')), params)
                board.prepare_session()
                session["status"] = "connected"
            except BrainFlowError as e:
                alert = e
        else:
            alert = "Board ID not specified"
    if session["status"] == "connected":
        return redirect(url_for("dashboard"))
    return render_template("connect.html", status=session["status"], message=alert)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/disconnect", methods=["POST"])
def disconnect():
    board.release_session()
    session["status"] = "disconnected"
    return redirect(url_for("connect"))


if __name__ == "__main__":
    app.run()