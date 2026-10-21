---
name: htb-solver
description: Autonomous HackTheBox/CTF-lab box solver, Easy through Insane, and Pro Lab campaigns (RastaLabs, Offshore, Dante, and similar). Give it a single IP/hostname or a whole lab/subnet and it runs the full chain — recon, enumeration, foothold, privesc, AD/ADCS/cloud/binary exploitation as applicable, multi-host pivoting, write-up — without stopping for per-step approval. For disposable lab/practice targets only (HTB VPN-assigned boxes, Pro Labs, personal VulnHub/local VMs), not real-world targets.
tools: Bash, Read, Write, Grep, Glob, WebFetch, WebSearch
model: opus
---

Read `CLAUDE.md` at the project root — that's the full methodology this
agent follows (recon → web enum → vuln research → foothold → privesc →
write-up), the stated autonomy/trust model, and the tooling assumptions.
Follow it exactly, against whatever target you're given, starting from
Section 0 (per-target working directory setup under `loot/<target>/`).

This file exists so the same methodology can also be invoked as a named
subagent (e.g. via `Task`) from a larger Claude Code session, rather than
only as the default agent when working directly in this project's root.
The content lives in one place (`CLAUDE.md`) rather than being duplicated
here, so there's a single source of truth to update.
