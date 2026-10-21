#!/usr/bin/env python3
"""Minimal proxy-free HTTP session client for the authorized HTB lab target.

Usage:
  client.py get  <path> [cookie_string]
  client.py post <path> <urlencoded_body> [cookie_string]
"""
import re
import socket
import sys
import os

HOST = os.environ["HTB_TARGET"]
PORT = 80


def request(method, path, body=None, cookie=None, extra=None):
    headers = [
        f"{method} {path} HTTP/1.1",
        f"Host: {HOST}",
        "User-Agent: Mozilla/5.0",
        "Accept: */*",
        "Connection: close",
    ]
    if cookie:
        headers.append(f"Cookie: {cookie}")
    if extra:
        headers.extend(extra)
    if body is not None:
        headers.append("Content-Type: application/x-www-form-urlencoded")
        headers.append(f"Content-Length: {len(body.encode())}")
    raw = "\r\n".join(headers) + "\r\n\r\n" + (body or "")

    s = socket.create_connection((HOST, PORT), timeout=20)
    s.settimeout(20)
    s.sendall(raw.encode())
    chunks = []
    while True:
        b = s.recv(8192)
        if not b:
            break
        chunks.append(b)
    s.close()
    return b"".join(chunks).decode(errors="replace")


def split(resp):
    head, _, body = resp.partition("\r\n\r\n")
    return head, body


def dechunk(head, body):
    if "chunked" not in head.lower():
        return body
    out, rest = [], body
    while rest:
        line, _, rest = rest.partition("\r\n")
        try:
            n = int(line.strip().split(";")[0], 16)
        except ValueError:
            break
        if n == 0:
            break
        out.append(rest[:n])
        rest = rest[n + 2:]
    return "".join(out)


def show(resp, limit=3000, text_only=True):
    head, body = split(resp)
    body = dechunk(head, body)
    print("=== HEAD ===")
    print(head)
    print("=== BODY ===")
    if text_only:
        b = re.sub(r"(?is)<style.*?</style>|<script.*?</script>", "", body)
        b = re.sub(r"(?s)<[^>]+>", " ", b)
        b = re.sub(r"[ \t]+", " ", b)
        b = "\n".join(l.strip() for l in b.splitlines() if l.strip())
        print(b[:limit])
    else:
        print(body[:limit])


if __name__ == "__main__":
    cmd = sys.argv[1]
    path = sys.argv[2]
    if cmd == "get":
        ck = sys.argv[3] if len(sys.argv) > 3 else None
        show(request("GET", path, cookie=ck))
    elif cmd == "post":
        data = sys.argv[3]
        ck = sys.argv[4] if len(sys.argv) > 4 else None
        show(request("POST", path, body=data, cookie=ck))
