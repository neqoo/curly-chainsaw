{\rtf1\ansi\ansicpg1252\cocoartf2907
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import socket\
import json\
\
PORT = 5005\
\
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)\
sock.settimeout(3)\
\
message = json.dumps(\{"type": "DISCOVER"\}).encode()\
\
# Broadcast sulla rete locale\
sock.sendto(message, ("255.255.255.255", PORT))\
\
print("[*] Ricerca del ricevitore Kali...")\
\
try:\
    data, addr = sock.recvfrom(4096)\
    response = json.loads(data.decode())\
\
    if response.get("type") == "DISCOVER_RESPONSE":\
        print(f"[+] Ricevitore trovato: \{addr[0]\}")\
    else:\
        print("[-] Risposta non riconosciuta")\
\
except socket.timeout:\
    print("[-] Nessun ricevitore trovato.")\
    print("Controlla rete, firewall e porta UDP.")\
\
finally:\
    sock.close()}