from pythonosc import dispatcher
from pythonosc import osc_server

OSC_PREFIX = "/franui"

def print_handler(marker_id, address, *args):
    print(f"[{marker_id}] Received OSC message at {address} with arguments {args}")

def print_handler_0(address, *args):
    print_handler(0, address, *args)

def print_handler_1(address, *args):
    print_handler(1, address, *args)

def print_handler_2(address, *args):
    print_handler(2, address, *args)

def test_handler(address, *args):
    print(f"Received test message at {address} with arguments {args}")

if __name__ == "__main__":
    # Set up the dispatcher to handle incoming OSC messages
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map(f"{OSC_PREFIX}/object/0/position/x", print_handler_0)
    dispatcher.map(f"{OSC_PREFIX}/object/0/position/y", print_handler_0)
    dispatcher.map(f"{OSC_PREFIX}/object/0/rotation/z", print_handler_0)
    dispatcher.map(f"{OSC_PREFIX}/object/0/scale", print_handler_0)
    dispatcher.map(f"{OSC_PREFIX}/object/0/scene/enters", print_handler_0)
    dispatcher.map(f"{OSC_PREFIX}/object/0/scene/leaves", print_handler_0)
    dispatcher.map(f"{OSC_PREFIX}/object/1/position/x", print_handler_1)
    dispatcher.map(f"{OSC_PREFIX}/object/1/position/y", print_handler_1)
    dispatcher.map(f"{OSC_PREFIX}/object/1/rotation/z", print_handler_1)
    dispatcher.map(f"{OSC_PREFIX}/object/1/scale", print_handler_1)
    dispatcher.map(f"{OSC_PREFIX}/object/1/scene/enters", print_handler_1)
    dispatcher.map(f"{OSC_PREFIX}/object/1/scene/leaves", print_handler_1)
    dispatcher.map(f"{OSC_PREFIX}/object/2/position/x", print_handler_2)
    dispatcher.map(f"{OSC_PREFIX}/object/2/position/y", print_handler_2)
    dispatcher.map(f"{OSC_PREFIX}/object/2/rotation/z", print_handler_2)
    dispatcher.map(f"{OSC_PREFIX}/object/2/scale", print_handler_2)
    dispatcher.map(f"{OSC_PREFIX}/object/2/scene/enters", print_handler_2)
    dispatcher.map(f"{OSC_PREFIX}/object/2/scene/leaves", print_handler_2)
    dispatcher.map("/test", test_handler)

    # Define the IP and port to listen on
    ip = "127.0.0.1"
    port = 7000

    # Create the server
    server = osc_server.BlockingOSCUDPServer((ip, port), dispatcher)
    print(f"Serving on {ip}:{port}")
    server.serve_forever()
