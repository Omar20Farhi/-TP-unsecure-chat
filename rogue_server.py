import zmq

# Intercepteur malveillant qui écoute le canal broadcast et affiche les données brutes
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:6667")
socket.setsockopt(zmq.SUBSCRIBE, b"")

print("[+] Listening for encrypted messages...")

while True:
    try:
        message = socket.recv()
        print(f"[ROGUE SERVER] Got encrypted data: {message}")
    except KeyboardInterrupt:
        break
