# Pulse
> Your Digital Identity, Extracted for the AI Era.

[![CI/CD Pipeline](https://github.com/ekinyuksel12/pulse/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/ekinyuksel12/pulse/actions/workflows/ci-cd.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**Pulse** is a modular data extraction suite. It unifies your professional footprint from GitHub, LinkedIn, and more into structured Markdown, optimized for LLM context ingestion, personal portfolios, and digital archival.

Whether you need to feed your technical history into a custom GPT, audit a developer portfolio, or build an OSINT professional profile, Pulse provides a reliable and developer-friendly pipeline.

---

## Installation

### Linux / macOS
```bash
curl -sSL https://raw.githubusercontent.com/ekinyuksel12/pulse/master/install.sh | bash
```

### Windows
1. Ensure Python 3.9+ is installed.
2. Run `pip install pulse-suite` or download the latest `pulse.exe` from [Releases](https://github.com/ekinyuksel12/pulse/releases).

---

## Extensible Architecture

Pulse is built on a Platform-Plugin model. Every digital identity is just a module away.

### Supported Now
- **GitHub**: Deep technical heartbeat, repository analytics, and inferred skill mapping.
- **LinkedIn**: Professional narrative, activity archival, and footprint extraction.

### Coming Soon
- **Reddit**: Engagement analysis and interest graphing.
- **Twitter/X**: Narrative tracking and social pulse.

---

## Usage

Pulse uses a centralized Auth Manager to store your credentials locally and securely.

### 1. Authenticate
```bash
pulse auth github
pulse auth linkedin
```

### 2. Extract
```bash
pulse github --username ekinyuksel12
pulse linkedin --profile-id teyuksel
```

---

## Features
- **Universal Interface**: One CLI (`pulse`) for every digital profile you own.
- **Secure Auth**: Local-only storage for API tokens and session cookies.
- **Async Performance**: Powered by `httpx` and asyncio for high-concurrency extraction.
- **LLM Ready**: Output is semantic Markdown, ready for RAG or few-shot context.

## Legal & Ethical Use

Pulse is designed for data portability. However, automated collection carries risks:

- **Platform Terms**: Many platforms (like LinkedIn) restrict automated scraping. Excessive use may result in account restrictions. 
- **Privacy**: Use Pulse only to archive data you are authorized to access.
- **Stealth**: We implement exponential backoff and jitter, but always prioritize platform health.

*Disclaimer: Pulse is provided "as is". The author is not responsible for any platform actions taken against your account.*

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
