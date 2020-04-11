from brainflow.board_shim import BoardShim, BrainFlowInputParams
from enviroment import connection_element_names
import json
import numpy as np

class MainBoard():

    def __init__(self):
        self.timeframe = 5
        self.status_message = "disconnected"
        self.connected = False
        self.emit_delay = 0.25
        self.data = None

    def set_board(self, board_id, params):
        self.board = BoardShim(board_id, params)
        return self

    def disconnect(self):
        self.board.release_session()
        self.connected = False
        self.data = None
        self.status_message = "disconnected"

    def connect(self):
        self.board.prepare_session()
        self.connected = True
        self.sampling_rate = self.board.get_sampling_rate(self.board.board_id)
        self.status_message = "connect"
        self.time = 0

    @staticmethod
    def extract_params(request):
        board_id = request.form.get(connection_element_names['board_id'])
        if board_id:
            board_id = int(board_id)
        log_level = int(request.form.get(connection_element_names['log_level']))
        params = BrainFlowInputParams()
        params.ip_port = int(request.form.get(connection_element_names['ip_port']))
        params.serial_port = request.form.getlist(connection_element_names['serial_port'])[-1]
        params.mac_address = request.form.getlist(connection_element_names['mac_address'])[-1]
        params.other_info = request.form.get(connection_element_names['other_info'])
        params.ip_address = request.form.get(connection_element_names['ip_address'])
        params.ip_protocol = int(request.form.get(connection_element_names['ip_protocol']))
        params.timeout = int(request.form.get(connection_element_names['timeout']))
        return board_id, log_level, params

    def get_json_data(self):
        data = self.board.get_board_data()
        channels = self.board.get_eeg_channels(self.board.board_id)
        if self.data is None:
            self.data = data[channels[0]:channels[-1]+1]
        else:
            self.data = np.concatenate((self.data, data[channels[0]:channels[-1]+1]),
                                       axis=1)[:, -(self.sampling_rate*self.timeframe):-1]
        self.time += self.emit_delay
        if data[channels[0]:channels[-1]+1].tolist()[0]:
            return {"data": self.data.tolist(),
                    "time": np.linspace(0, self.time,
                                        self.data.shape[-1])[-(self.sampling_rate*self.timeframe):-1].tolist()}
        return None
