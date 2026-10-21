#!/usr/bin/env python3
"""Banner + HTTP recon against an authorized HTB lab target."""
import socket
import ssl
import sys
import os
import urllib.request
import urllib.error

TARGET = os.environ["HTB_TARGET"]


def ssh_banner(host, port=22):
    try:
        s = socket.create_connection((host, port), timeout=8)
        s.settimeout(8)
        data = s.recv(256).decode(errors="replace").strip()
        s.close()
        return data
    except OSError as e:
        return f"error: {e}"


def http_get(url, host_header=None):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    if host_header:
        req.add_header("Host", host_header)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read()
            return r.status, dict(r.headers), body
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()
    except Exception as e:
        return None, {}, str(e).encode()


print("=== SSH BANNER (22) ===")
print(ssh_banner(TARGET))

print("\n=== HTTP GET / (80) ===")
status, headers, body = http_get(f"http://{TARGET}/")
print("Status:", status)
for k, v in headers.items():
    print(f"{k}: {v}")
print("\n--- BODY (first 4000 bytes) ---")
print(body[:4000].decode(errors="replace"))
print(f"\n[body length: {len(body)}]")
