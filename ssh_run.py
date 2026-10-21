#!/usr/bin/env python3
"""Authenticated SSH command runner for the authorized HTB target."""
import sys
import os
import paramiko

HOST = os.environ["HTB_TARGET"]
USER = sys.argv[1] if len(sys.argv) > 1 else os.environ["HTB_SSH_USER"]
PASS = os.environ["HTB_SSH_PASSWORD"]
CMD = sys.argv[2] if len(sys.argv) > 2 else "id; hostname; whoami"

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    c.connect(HOST, username=USER, password=PASS, timeout=25,
              allow_agent=False, look_for_keys=False)
    stdin, stdout, stderr = c.exec_command(CMD, get_pty=True, timeout=60)
    out = stdout.read().decode(errors="replace")
    err = stderr.read().decode(errors="replace")
    print("=== STDOUT ===")
    print(out)
    if err.strip():
        print("=== STDERR ===")
        print(err)
except paramiko.AuthenticationException:
    print("AUTH FAILED for", USER)
except Exception as e:
    print("ERROR:", e)
finally:
    c.close()
