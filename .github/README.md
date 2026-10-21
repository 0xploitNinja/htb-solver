# HTB Solver

An AI agent configuration for working through authorized Hack The Box machines and self-contained CTF labs with Claude Code or Codex CLI.

Give the agent a lab target and an explicit scope. Its instructions guide reconnaissance, enumeration, vulnerability research, initial access, privilege escalation, and an incremental technical write-up. The methodology covers Linux, Windows, web applications, Active Directory, cloud/container scenarios, binary analysis, and multi-host labs when relevant.

**This repository combines agent instructions with small Python lab helpers; it is not a standalone autonomous runtime or an MCP server.** The AI CLI interprets the instructions and uses tools installed on your machine. Outcomes depend on the model, available tools, permissions, network access, and target complexity; solving a machine is not guaranteed.

## How it works

1. **Load project context.** Claude Code uses `CLAUDE.md`; Codex CLI uses `AGENTS.md`. Both contain the same core methodology.
2. **Initialize working files.** The agent creates a target folder inside `loot/` for scan results, notes, progress, and the write-up.
3. **Discover the attack surface.** It is instructed to identify ports and services, enumerate applicable protocols, and inspect web applications where present.
4. **Investigate and validate findings.** It researches relevant vulnerabilities and records successful approaches and dead ends.
5. **Work through the lab.** Within the authorized scope, it attempts initial access, re-enumerates from new access contexts, and investigates privilege escalation.
6. **Document the result.** It updates evidence and notes along the way and produces a write-up explaining the attack path and lessons learned.

The workflow is iterative: a new credential, service, or foothold can trigger another round of enumeration. The multi-host guidance adds host, credential, and network tracking across a lab campaign.

## Repository structure

```text
htb-solver/
├── README.md                       # GitHub documentation
├── README.txt                      # Plain-text documentation
├── AGENTS.md                       # Codex CLI methodology
├── CLAUDE.md                       # Claude Code methodology
├── .claude/
│   └── agents/
│       └── htb-solver.md            # Optional Claude Code subagent definition
├── .gitignore                      # Excludes loot and common local secrets
└── loot/
    └── .gitkeep                     # Keeps the empty output folder in Git
```

The root also includes eight Python helpers and `requirements.txt`. There are no bundled exploit binaries, dependency lockfiles, installation scripts, or automated test suites.

## Requirements

- A Linux lab environment, such as Kali or Parrot, with terminal access.
- Claude Code or Codex CLI installed and authenticated through its supported setup.
- Access to your authorized lab, including the appropriate VPN connection when required.
- Permission for the chosen CLI to run the tools and write the working files it needs.
- Security tools installed separately for the services and techniques your lab requires.

Common tools referenced in the methodology:

| Area | Examples |
| --- | --- |
| Discovery | Nmap |
| Web enumeration | ffuf, Gobuster, Feroxbuster |
| Vulnerability research | SearchSploit |
| Authentication and service testing | Impacket, NetExec, John the Ripper, Hashcat |
| Windows and AD | BloodHound collectors, Certipy, Evil-WinRM, Responder |
| Binary analysis | GDB, Ghidra or radare2, pwntools, checksec |
| Lab pivoting | SSH forwarding, Chisel, Ligolo-ng |
| Cloud labs | AWS, Azure, or Google Cloud CLI as applicable |

These are external tools, not dependencies automatically installed by this repository. You do not need every tool for every target. The instructions ask the agent to check availability and record gaps.

## Getting started

Clone your repository and enter its root:

```bash
git clone https://github.com/0xploitNinja/htb-solver.git
cd htb-solver
```

The URL above assumes you publish under that account and repository name. Change it if you choose a different location.

Connect to your lab and confirm the assigned target and scope before starting.

### Claude Code

```bash
claude
```

Example prompt, replacing the address with your assigned lab IP:

```text
Work on my authorized HTB lab target 10.10.11.42.
Scope is this machine only. Follow CLAUDE.md and save evidence under loot/.
Do not expand to additional hosts without explicit scope.
```

### Codex CLI

```bash
codex
```

Use the same prompt with `AGENTS.md` in place of `CLAUDE.md`.

### Optional Claude Code subagent

The project includes `.claude/agents/htb-solver.md`, a named subagent definition that instructs the agent to read the root `CLAUDE.md`.

From your Claude Code session, ask it to use the `htb-solver` subagent for the authorized target. The definition specifies `model: opus`; adjust that field if your available model configuration requires it. How the subagent is selected depends on the CLI version and session capabilities.

## Output files

For a single target, the expected output is:

```text
loot/<target>/
├── progress.log       # Timestamped phase transitions and major findings
├── scans/             # Raw tool output
├── notes.md           # Findings, commands, attempts, and dead ends
└── writeup.md         # Recon summary, attack path, flags, and lessons
```

For a multi-host lab:

```text
loot/<lab-name>/
├── hosts.md           # Host inventory and current access
├── credentials.md     # Lab credentials and confirmed reuse
├── network-map.md     # Network segments and pivot state
└── hosts/
    └── <host>/        # Per-host progress, scans, and notes
```

These are instructed output conventions, not a validated application schema. Actual completeness depends on the agent run. Follow progress locally with:

```bash
tail -f loot/<target>/progress.log
```

To continue a previous attempt, explicitly ask the agent to read the existing notes and progress before taking further action.
