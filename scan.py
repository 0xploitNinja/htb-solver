#!/usr/bin/env python3
"""Threaded TCP connect scanner for authorized HTB lab targets."""
import socket
import sys
import os
from concurrent.futures import ThreadPoolExecutor

TARGET = sys.argv[1] if len(sys.argv) > 1 else os.environ["HTB_TARGET"]
START = int(sys.argv[2]) if len(sys.argv) > 2 else 1
END = int(sys.argv[3]) if len(sys.argv) > 3 else 65535
TIMEOUT = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
WORKERS = 600

open_ports = []


def probe(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    try:
        if s.connect_ex((TARGET, port)) == 0:
            open_ports.append(port)
            print(f"OPEN {port}", flush=True)
    except OSError:
        pass
    finally:
        s.close()


with ThreadPoolExecutor(max_workers=WORKERS) as pool:
    pool.map(probe, range(START, END + 1))

print("PORTS:" + ",".join(str(p) for p in sorted(open_ports)))
