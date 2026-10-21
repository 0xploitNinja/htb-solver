#!/usr/bin/env python3
"""Raw-socket HTTP request (no proxy autodetection) for authorized HTB lab target."""
import socket
import sys
import os

host = sys.argv[1] if len(sys.argv) > 1 else os.environ["HTB_TARGET"]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 80
path = sys.argv[3] if len(sys.argv) > 3 else "/"

req = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "User-Agent: Mozilla/5.0\r\n"
    "Accept: */*\r\n"
    "Connection: close\r\n\r\n"
)

try:
    s = socket.create_connection((host, port), timeout=15)
    s.settimeout(15)
    s.sendall(req.encode())
    chunks = []
    while True:
        b = s.recv(8192)
        if not b:
            break
        chunks.append(b)
    s.close()
    data = b"".join(chunks)
    print(f"[{len(data)} bytes from {host}:{port}{path}]")
    print(data[:6000].decode(errors="replace"))
except OSError as e:
    print(f"CONNECT/IO ERROR to {host}:{port} -> {e}")
