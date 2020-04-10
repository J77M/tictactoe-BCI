from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, LogLevels, IpProtocolType

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.debug = True

Session(app)


@app.route("/connect", methods=["GET", "POST"])
def index():
    # check connection - if not connected render : connect else dashboard
    if request.method == "POST":
        print(request.args)
        board_id = request.form.get('board_id')
        serial_port = request.form.getlist('serial_port')
        mac_address = request.form.getlist('mac_address')
        log_level = request.form.get("log_level")
        ip_protocol_types = request.form.get("ip_protocol_type")
        timeout = request.form.get("timeout")
        alert = "board id : {}; serial port : {}; mac address : {}; log level : {}; ip protocol types : {};" \
                " timeout : {}".format(board_id, serial_port, mac_address, log_level, ip_protocol_types, timeout)
    else:
        alert = None
    return render_template("connect.html", boards=BoardIds, log_levels=LogLevels,
                           ip_protocol_types=IpProtocolType, message=alert)



if __name__ == "__main__":
    app.run()