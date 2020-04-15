import numpy as np
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from tttBCI.enviroment import connection_element_names


class MainBoard():

    def __init__(self):
        self.status_message = "disconnected"
        self.timeframe = 30
        self.connected = False
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

    def process_data(self):
        data = self.board.get_board_data()
        eeg_channels = self.board.get_eeg_channels(self.board.board_id)
        df = pd.DataFrame(np.transpose(data))
        if self.data is None:
            self.data = df[-(self.sampling_rate*self.timeframe):-1]
        else:
            print(self.data.shape)
            self.data = pd.concat([self.data, df])[-(self.sampling_rate*self.timeframe):-1]
        print(self.data.shape)
        for channel in eeg_channels:
            DataFilter.perform_highpass(self.data[channel].to_numpy(), BoardShim.get_sampling_rate(self.board.board_id), 1.0, 4,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_lowpass(self.data[channel].to_numpy(), BoardShim.get_sampling_rate(self.board.board_id), 30.0, 4,
                                FilterTypes.BUTTERWORTH.value, 0)
        return self.data

    def add_timestamps(self, events_timestamps):
       timestamp_channel = self.board.get_timestamp_channel(self.board.board_id)
       timestamps_vals = [None for i in range(self.data.shape[0])]
       for event_timestamp in events_timestamps:
           index = (np.abs(np.int64(self.data[timestamp_channel]*1000) - event_timestamp)).argmin()
           print(index, np.int64(self.data[timestamp_channel]*1000)[index], event_timestamp)
           timestamps_vals[index] = True
       return timestamps_vals
