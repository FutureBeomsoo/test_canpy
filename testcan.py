import can
import time

filters = [
    {"can_id": 0x201, "can_mask": 0x7FF, "extended": False},
    {"can_id": 0x202, "can_mask": 0x7FF, "extended": False},
]

# with can.ThreadSafeBus(interface='socketcan', channel='vcan0', bitrate=500000 ,can_filters=filters) as bus:
#     msg = can.Message(
#         arbitration_id=0x301,
#         data=[0, 25, 0, 1, 3, 1, 4, 1],
#         is_extended_id=True
#     )
#     print_listener = can.Printer()
#     can.Notifier(bus, [print_listener])
#     try:
#         bus.send(msg)
#         print(f"Message sent on {bus.channel_info}")
#     except can.CanError:
#         print("Message NOT sent")
    
#     for msg1 in bus:

#         print(f"Message recive on {msg1}")

def print_message(msg: can.Message) -> None:
    """Regular callback function. Can also be a coroutine."""
    print(f"Message print_message on {msg}")

def main():
    with can.ThreadSafeBus(interface='socketcan', channel='vcan0', bitrate=500000 ,can_filters=filters,receive_own_messages=True)as bus:
        # print_listener = can.Printer()
        # can.Notifier(bus, [print_listener])

        msg1 = can.Message(
            arbitration_id=0x301,
            data=[0, 25, 0, 1, 3, 1, 4, 1],
            is_extended_id=True
        )
        reader = can.BufferedReader()
        listeners: List[MessageRecipient] = [
            # print_message,  # Callback function
            reader,  # AsyncBufferedReader() listener
            # can.Logger("TestLogFile.log"),  # Regular Listener object
        ]
        
        can.Notifier(bus, listeners)


        bus.send(can.Message(arbitration_id=1, is_extended_id=False))
        bus.send(can.Message(arbitration_id=2, is_extended_id=False))
        bus.send(can.Message(arbitration_id=1, is_extended_id=False))

        time.sleep(1.0)

        msg = bus.recv()
        print(f"Message recive on {msg}")
        time.sleep(1.0)

        msg = bus.recv()
        print(f"Message recive on {msg}")
        # listeners(msg1)
        # listeners.on_message_received(msg)
        # reader = can.BufferedReader()
        # print(f"Message recive on {msg}")
        while 1:
            msg1=reader.get_message(timeout=0.5)
            print (f"Message reader on {msg1}")
        # reader.on_message_received(msg)
        # msg1=reader.get_message(timeout=0.5)
        # print (f"Message reader on {msg1}")
        # # print_listener(msg)
        # # print_listener.stop()


if __name__ == "__main__":
    main()

