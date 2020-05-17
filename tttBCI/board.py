import numpy as np
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from tttbci.enviroment import connection_element_names


class MainBoard():

    def __init__(self):
        self.timeframe = 30
        self.connection = False
        self.data = None

    def set_board(self, board_id, params):
        self.board = BoardShim(board_id, params)
        return self

    def disconnect(self):
        self.board.release_session()
        self.connection = False
        self.data = None

    def connect(self):
        self.board.prepare_session()
        self.connection = True
        self.sampling_rate = self.board.get_sampling_rate(self.board.board_id)

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

    def add_stim_channel(self, stim_data, data):
        '''
        add stimulation channels for training
        :param stim_data: event data from socketio - event_data["data"]
        :param data: transposed data from eeg
        :return: stim_channel1 - row and column match, stim_channel2 : row and column doesnt match
        '''
        _data = np.transpose(data)
        timestamp_channel = self.board.get_timestamp_channel(self.board.board_id)
        stim_channel1 = [0 for i in range(_data.shape[0])]
        stim_channel2 = [0 for i in range(_data.shape[0])]
        for dict in stim_data:
            event_timestamp = dict["timestamp"]
            index = (np.abs(np.int64(_data[:,timestamp_channel]*1000) - event_timestamp)).argmin()
            # print(index, np.int64(_data[:,timestamp_channel] * 1000)[index], event_timestamp) TODO: dont delete
            if dict["row"] == dict["selected-row"] or dict["column"] == dict["selected-column"]:
                stim_channel1[index] = 1
            else:
                stim_channel2[index] = 1
        return np.array(stim_channel1), np.array(stim_channel2)

    def save_stim_data(self, path, stim_channel1, stim_channel2, data):
        ''''
        Saves eeg data with correspondent timestamps and stimulation channel
        :param stim_channel1: np array from stim_channel1
        :param stim_channel2: np array from stim_channel2
        :param data: raw data from self.board.get_board_data()
        '''
        _data = np.transpose(data)
        timestamp_channel = self.board.get_timestamp_channel(self.board.board_id)
        eeg_channels = self.board.get_eeg_channels(self.board.board_id)
        to_remove = [i for i in range(_data.shape[-1]) if i not in eeg_channels and i != timestamp_channel]
        data = np.delete(_data, to_remove, axis=1)
        df = pd.DataFrame(data, columns=["chan {}".format(i+1) for i in range(len(eeg_channels))] + ["timestamps"])
        df["stim_channel1"] = stim_channel1
        df["stim_channel2"] = stim_channel2
        df.to_csv(path,  sep=',')

