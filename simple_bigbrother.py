import zmq

# Écoute tous les messages du broadcast
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:6667")
socket.setsockopt(zmq.SUBSCRIBE, b"")

print("[BIGBROTHER] Listening on port 6667...")

while True:
    try:
        message = socket.recv()
        print(f"[INTERCEPTED] {message}")
    except KeyboardInterrupt:
        break
