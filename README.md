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

## Python helpers in this version

These are independent utilities from a specific lab attempt. The agent instructions do not automatically call or orchestrate them. `upload.py` and `sh.py` assume particular application routes and are not generic upload or shell tools.

| File | Purpose | Configuration / limitations |
| --- | --- | --- |
| `scan.py` | Threaded IPv4 TCP connect port scan | Target, start port, end port, timeout as positional arguments; 600 workers |
| `http_recon.py` | SSH banner and HTTP root-page inspection | `HTB_TARGET`; ports 22 and 80; urllib may use configured proxies |
| `raw_http.py` | Raw HTTP GET | Host, port, path as positional arguments; plain HTTP |
| `extract.py` | Extract HTML links, forms, comments, inputs, and text | Host, port, path; regex-based extraction, no JavaScript execution |
| `client.py` | HTTP GET/POST with optional explicit cookies | `HTB_TARGET`; port 80; raw socket client, no cookie jar or TLS |
| `upload.py` | Upload a PHP command-execution payload in the lab | `HTB_TARGET`, `HTB_COOKIE`; application-specific admin route and form fields |
| `sh.py` | Send a command to an existing lab web shell | `HTB_TARGET`; assumes `/uploads/htbshell.php` exists |
| `ssh_run.py` | Run a command over authenticated SSH | `HTB_TARGET`, `HTB_SSH_USER`, `HTB_SSH_PASSWORD`; uses Paramiko |

Set the target in the same terminal before using helpers without an explicit target argument:

```bash
export HTB_TARGET="YOUR_ASSIGNED_LAB_IP"
python3 scan.py "$HTB_TARGET" 1 1024 1
python3 http_recon.py
python3 raw_http.py "$HTB_TARGET" 80 /
python3 extract.py "$HTB_TARGET" 80 /
python3 client.py get /
```

For SSH support only, create an isolated environment and install the dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
export HTB_SSH_USER="YOUR_LAB_USERNAME"
read -rs -p "Lab SSH password: " HTB_SSH_PASSWORD
export HTB_SSH_PASSWORD
printf '\n'
python3 ssh_run.py "$HTB_SSH_USER" "id"
unset HTB_SSH_PASSWORD
```

The SSH helper currently accepts unknown host keys automatically. Verify the lab host identity independently before use. Its password is supplied through the environment rather than committed code or a password argument.

The upload helper requires `HTB_COOKIE` to be set locally. Review its route, form fields, payload, and filename first. Its default filename is `shell.php`, whereas `sh.py` expects `htbshell.php`; those names must match for that pair to work. These scripts are preserved as lab examples rather than rewritten into a general exploitation framework.

The raw HTTP utilities have limited response handling; they do not provide full browser behavior, redirects, robust binary/chunk decoding, or TLS. The helpers print output to the terminal; redirect output into `loot/` if you want to retain it. Target values are configuration, not enforced scope controls.

The public copy replaces the original target defaults with `HTB_TARGET` and removes the embedded SSH credential and admin cookie. Supply your own authorized lab values locally.

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

## Scope and permissions

Use only on disposable lab targets you are authorized to test. For multi-host labs, explicitly provide the permitted hosts/subnets; discovery alone does not grant authorization to test another host.

The instructions request autonomous operation, but **there is no programmatic target allowlist, scope validator, approval system, or sandbox in this repository**. Lab-looking IP addresses and hostnames do not prove authorization. CLI permission prompts and execution restrictions still apply; these instruction files do not bypass them.

Review the methodology before running it. It directs active testing and may alter lab target state. It also instructs the agent to stop when an environment appears to contain real production systems or real user data. That is an instruction to the model, not an enforced technical control.

## Keeping lab data out of GitHub

`.gitignore` excludes generated `loot/` contents, common credential/key files, VPN files, and local Claude settings. Only `loot/.gitkeep` is intended to be tracked in that directory.

Do not force-add lab output. Review the staged diff before publishing; ignore rules cannot remove files already committed and do not detect secrets written into otherwise tracked Markdown files. Keep flags, captured credentials, and unredacted lab write-ups local. Check the platform's publication rules before sharing any walkthrough.

## Publishing to GitHub

Create an empty repository named `htb-solver` on GitHub. Leave its automatic README, license, and `.gitignore` options unchecked because this folder already includes documentation and ignore rules.

From the extracted project folder:

```bash
git init
git branch -M main
git add README.md README.txt AGENTS.md CLAUDE.md .gitignore requirements.txt .claude/agents/htb-solver.md loot/.gitkeep client.py extract.py http_recon.py raw_http.py scan.py sh.py ssh_run.py upload.py
git diff --cached --stat
git diff --cached
```

After reviewing the staged files:

```bash
git commit -m "Add HTB Solver agent configuration and documentation"
git remote add origin https://github.com/0xploitNinja/htb-solver.git
git push -u origin main
```

Change the URL if needed. Authenticate using your configured GitHub credential manager, token, or SSH setup. If this folder already has a Git repository or an `origin` remote, inspect `git status` and `git remote -v` before adapting these commands.

Suggested repository description:

> AI agent instructions and Python helpers for authorized HTB/CTF labs with Claude Code or Codex, enumeration workflows, and technical write-ups.

Suggested topics: `hackthebox`, `ctf`, `cybersecurity`, `claude-code`, `codex`, `ai-agent`, `penetration-testing`.

## Customization and limitations

- Keep the shared methodology in `CLAUDE.md` and `AGENTS.md` aligned when editing it. `AGENTS.md` also contains a Codex-specific introductory paragraph.
- The Claude subagent wrapper reads `CLAUDE.md`; it does not contain a separate methodology.
- Model reasoning can be incomplete or incorrect. Verify findings and resulting write-ups.
- There is no automatic flag submission, scoring integration, tool installation, or guaranteed completion time.
- This package has been reviewed for documentation and repository structure, and the Python files passed syntax parsing; it has not been validated by running network actions or an end-to-end HTB solve.

## License and affiliation

No license is included. Add a license of your choice if you want to grant explicit reuse and distribution rights.

This is an independent project and is not affiliated with or endorsed by Hack The Box, Anthropic, or OpenAI.
