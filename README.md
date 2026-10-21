# htb-solver

An autonomous HackTheBox / CTF-lab box-solving agent. Give it one target
— an IP or hostname — and it runs the full chain itself: full-port recon,
service enumeration, web testing if applicable, vulnerability research,
initial foothold, privilege escalation, and a final write-up with both
flags. The same methodology scales from Easy boxes up through Insane
(iterative re-enumeration, exploit adaptation, binary exploitation/
reverse engineering, credential reuse) and up to full Pro Lab campaigns
(RastaLabs, Offshore, Dante, Zephyr, APTLabs, Cybernetics, and similar —
multi-host, multi-domain, ADCS abuse, trust-relationship exploitation,
lab-wide credential/host tracking). No per-step approval gate — that's a
deliberate, different trust model from the gated NayaPay engagement
tooling in the sibling `nayapay-redteam-agent` project, appropriate here
specifically because HTB-style targets are disposable, purpose-built
practice boxes.

**Works with both Claude Code and Codex** — the same methodology lives in
two files so each tool picks it up automatically:

- `CLAUDE.md` — Claude Code reads this as project context automatically.
  There's also `.claude/agents/htb-solver.md`, a thin named-subagent
  wrapper around the same file, for invoking it as a subagent from a
  larger session rather than only as the default agent.
- `AGENTS.md` — Codex CLI's equivalent convention, same content.

Both files are kept in sync manually since they're near-duplicates by
necessity (Codex has no subagent/delegation mechanism to point at a
shared file the way Claude Code does) — if you edit the methodology,
update both.

## Usage

**Claude Code:**
```
cd htb-solver
claude
> 10.10.11.42, go
```

**Codex:**
```
cd htb-solver
codex
> 10.10.11.42, go
```

Either way, output lands in `loot/10.10.11.42/` — `progress.log` (live
status), `scans/` (raw tool output), `notes.md` (working notes), and
`writeup.md` (the final deliverable). For a Pro Lab or any multi-host
engagement, give it the lab/subnet instead of a single IP; output then
lands under `loot/<lab-name>/` with a `hosts/<host>/` subfolder per
machine plus lab-wide `hosts.md`, `credentials.md`, and
`network-map.md` tracking files (see `CLAUDE.md`/`AGENTS.md` for the
full Pro Labs section).

## Trust model — read this before pointing it at anything

This agent does not validate that a target is actually a disposable lab
box — no IP-range check, no hostname pattern match. That's intentional
(see `CLAUDE.md`'s opening section for the reasoning), which also means
the safety net here is entirely you: only point this at boxes you're
actually authorized to attack under your own HTB VPN connection or a
personal lab VM. This is not the tool to reach for against anything with
real users or real data — that's what the gated `nayapay-redteam-agent`
project is for, with a written scope document and per-step approval on
anything active.

## Tooling

Same core toolkit as the NayaPay web/host specialists — see
`TOOLING_SETUP.md` in the sibling project if you've already set that up,
most of it carries over. `nmap`, `ffuf`/`gobuster`/`feroxbuster`,
`searchsploit`, `impacket`, `hashcat`/`john`, `netexec` cover most HTB
boxes; add `linpeas`/`winpeas` if you want the automated local-enum
sweep rather than the manual equivalent this agent falls back to.

For Hard/Insane boxes and Pro Labs specifically: `gdb`+`pwndbg`/`GEF`,
Ghidra or radare2, `pwntools`, `ROPgadget`, `checksec` (binary
exploitation); `certipy` (ADCS), `mimikatz`/`Rubeus`, `evil-winrm`,
`bloodhound-python`/`SharpHound`, `Responder` (AD/Pro Lab campaigns);
`chisel`/`ligolo-ng`/`sshuttle` (pivoting).
