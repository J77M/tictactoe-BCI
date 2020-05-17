from brainflow.board_shim import BoardIds, LogLevels, IpProtocolType

boards_properties = {
    "boards": BoardIds,
    "log_levels": LogLevels,
    "ip_protocol_types": IpProtocolType
}

connection_element_names = {
    "ip_port": "ip_port",
    "serial_port": "serial_port",
    "mac_address": "mac_address",
    "other_info": "other_info",
    "ip_address": "ip_address",
    "ip_protocol": "ip_protocol_type",
    "timeout": "timeout",
    "board_id": "board_id",
    "log_level": "log_level"
}

events_values = {
    "events_per_cycle": 3,
    "cycles": 2,
    "interval": 50,
}