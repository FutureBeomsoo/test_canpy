import cantools
import can
import time

filters = [
    {"can_id": 0x201, "can_mask": 0x7FF, "extended": False},
    {"can_id": 0x202, "can_mask": 0x7FF, "extended": False},
    {"can_id": 496, "can_mask": 0x7FF, "extended": False},
]

db = cantools.database.load_file('motohawk.dbc')
print (f'Message List : {db.messages}')


with can.ThreadSafeBus(interface='socketcan', channel='vcan0', bitrate=500000 ,can_filters=filters,receive_own_messages=True) as bus :

    test_send_msg = db.get_message_by_name ('ExampleMessage')
    print (f'test_send_msg : {test_send_msg}')
    encode_data = test_send_msg.encode({'Temperature': 231.12, 'AverageRadius': 1.3, 'Enable': 1})
    print (f'encode_data : {encode_data}')
    print (f'test_send_msg_encode_data : {test_send_msg}')
    endode_msg = can.Message(arbitration_id = test_send_msg.frame_id, data = encode_data,is_extended_id=False )
    print (f'send_msg : {endode_msg}')
    bus.send(endode_msg)

    receive_msg = bus.recv()
    decode_msg = db.decode_message(receive_msg.arbitration_id, receive_msg.data)
    print (f'decode_msg : {decode_msg}')
    Temperature = decode_msg['Temperature']
    AverageRadius = decode_msg['AverageRadius']
    Enable = decode_msg['Enable']

    print (f'Temperature : {Temperature} AverageRadius : {AverageRadius} Enable : {Enable}')
    print (f'{type(cantools.database.namedsignalvalue.NamedSignalValue)}')
    