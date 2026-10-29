
import json
PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(3)
message = json.dumps(\{"type": "DISCOVER"\}).encode()
# Broadcast sulla rete locale
sock.sendto(message, ("255.255.255.255", PORT))

print("[*] Ricerca del ricevitore Kali...")

try:
    data, addr = sock.recvfrom(4096)
    response = json.loads(data.decode())

    if response.get("type") == "DISCOVER_RESPONSE":
        print(f"[+] Ricevitore trovato: \{addr[0]\}")
    else:
        print("[-] Risposta non riconosciuta")

except socket.timeout:
    print("[-] Nessun ricevitore trovato.")
    print("Controlla rete, firewall e porta UDP.")

finally:
    sock.close()}
