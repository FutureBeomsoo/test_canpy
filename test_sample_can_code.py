import can
import asyncio
import time

filters = [
    {"can_id": 0x201, "can_mask": 0x7FF, "extended": False},
    {"can_id": 0x202, "can_mask": 0x7FF, "extended": False},
]

def callback_fnc( msg : can.Message) :
    print(f"Message Receive on : {msg}")

async def _receiver() -> None:


    

def main() :
    with can.ThreadSafeBus(interface='socketcan', channel='vcan0', bitrate=500000 ,can_filters=filters,receive_own_messages=True)as bus:

        send_msg = can.Message(
            arbitration_id=0x301,
            data=[0, 25, 0, 1, 3, 1, 4, 1],
            is_extended_id=True
        )
        reader = can.BufferedReader()
        logger = can.Logger("TestLogFile.log")


        listeners = [
            callback_fnc,  # Callback function
            reader,  # AsyncBufferedReader() listener
            logger,  # Regular Listener object
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




if __name__ == "__main__":
    main()