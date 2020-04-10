from brainflow.board_shim import BoardShim, BrainFlowInputParams
from enviroment import connection_element_names

class MainBoard():

    def __init__(self):
        self.status_message = "disconnected"
        self.connected = False

    def set_board(self, board_id, params):
        self.board = BoardShim(board_id, params)
        return self

    def disconnect(self):
        self.board.release_session()
        self.connected = False
        self.status_message = "disconnected"

    def connect(self):
        self.board.prepare_session()
        self.connected = True
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