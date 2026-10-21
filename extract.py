#!/usr/bin/env python3
"""Fetch a page over a raw socket and extract links/forms/comments/text."""
import re
import socket
import sys
import os

host = sys.argv[1] if len(sys.argv) > 1 else os.environ["HTB_TARGET"]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 80
path = sys.argv[3] if len(sys.argv) > 3 else "/"


def fetch(host, port, path):
    req = (
        f"GET {path} HTTP/1.1\r\nHost: {host}\r\n"
        "User-Agent: Mozilla/5.0\r\nAccept: */*\r\nConnection: close\r\n\r\n"
    )
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
    return b"".join(chunks).decode(errors="replace")


raw = fetch(host, port, path)
head, _, body = raw.partition("\r\n\r\n")
print("=== STATUS LINE ===")
print(head.splitlines()[0] if head else "(none)")

# strip style/script blocks for the text view
text_src = re.sub(r"(?is)<style.*?</style>", "", body)
text_src = re.sub(r"(?is)<script.*?</script>", "", text_src)

print("\n=== HTML COMMENTS ===")
for c in re.findall(r"<!--(.*?)-->", body, re.S):
    if c.strip():
        print("  #", c.strip()[:300])

print("\n=== LINKS (href) ===")
for h in sorted(set(re.findall(r'href=["\']([^"\']+)["\']', body, re.I))):
    print("  ", h)

print("\n=== SRC / ACTION ===")
for h in sorted(set(re.findall(r'(?:src|action)=["\']([^"\']+)["\']', body, re.I))):
    print("  ", h)

print("\n=== FORMS ===")
for f in re.findall(r"(?is)<form.*?</form>", body):
    print("  ", re.sub(r"\s+", " ", f)[:600])

print("\n=== INPUTS ===")
for i in set(re.findall(r"(?i)<input[^>]*>", body)):
    print("  ", re.sub(r"\s+", " ", i))

print("\n=== VISIBLE TEXT ===")
txt = re.sub(r"(?s)<[^>]+>", " ", text_src)
txt = re.sub(r"[ \t]+", " ", txt)
lines = [l.strip() for l in txt.splitlines() if l.strip()]
print("\n".join(lines[:80]))
