import socket
import json
import uuid
import platform

PORT = 5005
TIMEOUT = 3

def get_local_ip():
    """Determina l'IP usato dall'interfaccia di rete attiva."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Non invia dati applicativi; determina l'interfaccia scelta
        # dal sistema operativo per raggiungere una destinazione esterna.
        sock.connect(("192.0.2.1", 80))
        return sock.getsockname()[0]
    except OSError:
        return "N/D"
    finally:
        sock.close()

def get_mac():
    """Restituisce l'indirizzo MAC associato al nodo."""
    value = uuid.getnode()
    return ":".join(
        f"{(value >> shift) & 0xff:02X}"
        for shift in range(40, -1, -8)
    )

def discover_receiver():
    message = json.dumps({"type": "DISCOVER"}).encode("utf-8")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(TIMEOUT)

    try:
        sock.sendto(message, ("255.255.255.255", PORT))
        print("[*] Ricerca del ricevitore nella rete locale...")

        data, addr = sock.recvfrom(4096)
        response = json.loads(data.decode("utf-8"))

        if response.get("type") == "DISCOVER_RESPONSE":
            print(f"[+] Ricevitore trovato: {addr[0]}")
            return addr[0]

        print("[-] Risposta non riconosciuta.")
        return None

    except socket.timeout:
        print("[-] Ricevitore non trovato.")
        print("    Controlla che Kali sia in ascolto e che")
        print("    entrambi i dispositivi siano sulla stessa LAN.")
        return None

    except (OSError, ValueError, UnicodeDecodeError) as exc:
        print(f"[-] Errore durante il discovery: {exc}")
        return None

    finally:
        sock.close()

def main():
    hostname = socket.gethostname()
    ip = get_local_ip()
    mac = get_mac()

    print(f"Sistema operativo: {platform.system()}")
    print(f"Hostname:          {hostname}")
    print(f"IP locale:         {ip}")
    print(f"MAC rilevato:      {mac}")

    receiver = discover_receiver()

    if receiver:
        print(f"\nRicevitore individuato: {receiver}")
        print("Discovery completato.")

if __name__ == "__main__":
    main()