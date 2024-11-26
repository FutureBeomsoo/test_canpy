import can
import cantools
import asyncio
import time

_rcv_filters = [
    {"can_id": 0x201, "can_mask": 0x7FF, "extended": False},
    {"can_id": 0x202, "can_mask": 0x7FF, "extended": False},
]

_send_list = []

db = cantools.database.load_file('motohawk.dbc')

async def callback_fnc( msg : can.Message) -> None:
    print(f"Message Receive on : {msg}")


def set_periodic_send(bus,msg : can.Message) -> can.CyclicSendTaskABC :

    task = bus.send_periodic(msg, 0.20)
    assert isinstance(task, can.CyclicSendTaskABC)

    return task

def _periodic_stop(task : can.CyclicSendTaskABC) -> None :

    try :
        isinstance(task, can.CyclicSendTaskABC)
    except:
        print (f"Can not stop to {task}")
    else:
        task.stop()
        print (f"Stop to {task}")

def _modifying_data(task : can.CyclicSendTaskABC, msg : can.Message) -> None :
    if not isinstance(task, can.ModifiableCyclicTaskABC):
        print("This interface doesn't seem to support modification")
        return
    task.modify_data(msg)

async def set_receiver(bus) -> None:

    reader = can.AsyncBufferedReader()
    logger = can.Logger("TestLogFile.log")

    listeners = [
        callback_fnc,  # Callback function
        reader,  # AsyncBufferedReader() listener
        logger,  # Regular Listener object
    ]
    loop = asyncio.get_running_loop()

    can.Notifier(bus, listeners)


    

async def main() :
    with can.ThreadSafeBus(interface='socketcan', channel='vcan0', bitrate=500000 ,can_filters=_rcv_filters,receive_own_messages=True)as bus:

        send_msg = can.Message(
            arbitration_id=0x301,
            data=[0, 25, 0, 1, 3, 1, 4, 1],
            is_extended_id=True
        )

        await set_receiver(bus)


if __name__ == "__main__":
    asyncio.run(main())