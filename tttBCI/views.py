from flask import render_template, request, redirect, url_for
from brainflow.board_shim import BrainFlowError
from tttBCI import app, DEVICE, socketio
from tttBCI.enviroment import boards_properties, connection_element_names

@app.context_processor
def variables_setup():
    return {"boards_properties": boards_properties, "connection_element_names" : connection_element_names}

@app.route("/connect", methods=["GET", "POST"])
def connect():
    alert = None
    # check connection - if not connected render : connect else dashboard
    if request.method == "POST":
        board_id, log_level, params = DEVICE.extract_params(request)
        if board_id:
            try:
                DEVICE.set_board(board_id, params)
                DEVICE.board.set_log_level(log_level)
                DEVICE.connect()
                DEVICE.board.start_stream()
            except BrainFlowError as e:
                alert = e
        else:
            alert = "Board ID not specified"
    if DEVICE.connection:
        return redirect(url_for("dashboard"))
    return render_template("connect.html", message=alert)

@app.route("/dashboard")
def dashboard():
    if DEVICE.connection:
        return render_template("dashboard.html")
    return redirect(url_for("connect"))

@app.route("/disconnect", methods=["POST"])
def disconnect():
    if DEVICE.connection:
        DEVICE.board.stop_stream()
        DEVICE.disconnect()
        return redirect(url_for("connect"))
    return redirect(url_for("connect"))

# @socketio.on("start-stream")
# def data_stream_control(data):
#     if data["action"] == "start":
#         DEVICE.board.start_stream()
#     else:
#         DEVICE.board.stop_stream()

@socketio.on("event-data")
def data_stream_control(event_data):
    event_data = event_data["data"]
    data = DEVICE.process_data()
    timestamps = []
    for dict in event_data:
        timestamps.append(dict["timestamp"])
    timestamps = DEVICE.add_timestamps(timestamps)
    eeg_channels = DEVICE.board.get_eeg_channels(DEVICE.board.board_id)
    # axes = data[eeg_channels].plot(subplots=True)
    # for i in range(len(timestamps)):
    #     if timestamps[i]:
    #         for ax in axes:
    #             ax.axvline(x=i)
    # plt.show()