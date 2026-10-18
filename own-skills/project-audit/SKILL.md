---
name: project-audit
description: Audit a project for security vulnerabilities, leaked secrets, vulnerable dependencies and bugs — quick or full mode, severity-ranked report, no code changes.
---

# Project Audit — security and bugs

Reply to the user in their language (Russian by default). Do NOT modify the project's code: only read, run analyzers and write the report. Any fix happens only after the user confirms it, finding by finding.

## 0. Start
1. If the mode is not given, ask: **quick** (~5 min) or **full** (everything below).
2. Locate the project: attached files, connected folder, or GitHub repo. If there is no source, ask for one.
3. Before running anything, list what will be run and state that nothing in the project on disk changes (scanners are installed in the working environment, not in the project). Wait for confirmation.
4. Work on a copy of the project in the working directory.

## 1. Recon (both modes)
- Identify the stack: JS/TS (Three.js, browser games, static sites), Python, Flutter/Dart, other.
- Find entry points: index.html, main.*, server routes, APIs, JSON/level loaders, input forms.
- Note what is deployed (GitHub Pages, server).
- full: short threat model — what is valuable (data, accounts, server access), who could attack (random visitor, other user, malicious package), main trust boundaries (browser ↔ server, app ↔ device, project ↔ dependencies). Use it to prioritize the rest of the audit.

## 2. Secrets (both modes)
- `gitleaks detect` (or `trufflehog filesystem`) over the code and git history.
- Manual search: API keys, tokens, passwords, private URLs, `.env` files, keys in client-side JS.
- Static sites: everything in the browser is public — any secret in the client is Critical.

## 3. Dependencies (both modes)
- JS: `npm audit --json`; Python: `pip-audit`; general: `osv-scanner -r .`.
- Flag CDN libraries with no pinned version or no SRI.
- quick: High/Critical CVEs only.
- full, supply chain:
  - `postinstall`/`preinstall`/`prepare` scripts in dependencies and their sources;
  - typosquatting: package names one letter off from popular ones, very new or tiny-download packages;
  - lockfile present and committed; dependencies pinned;
  - SBOM via `syft . -o table` (summary only in the report).
- full, licenses: `license-checker --summary` (JS), `pip-licenses` (Python). Flag GPL/AGPL/unknown licenses if the project is published or commercial; flag asset licenses (models, textures, fonts, sounds) when a license file is missing.

## 4. Static code analysis
- quick: `semgrep --config auto`, High/Error findings only.
- full: `semgrep` with stack rulesets (p/javascript, p/python, p/secrets, p/owasp-top-ten) + `bandit -r` for Python + manual review:
  - XSS: innerHTML, outerHTML, document.write, insertAdjacentHTML fed with untrusted data;
  - eval, new Function, setTimeout with a string;
  - loading JSON/levels/saves without validation; prototype pollution;
  - postMessage without origin checks;
  - backend: authentication, authorization, CORS, path traversal, command and SQL injection, subprocess with shell=True, unsafe deserialization (pickle), debug modes left on;
  - sensitive data in localStorage;
  - home-made crypto (e.g. password locks for GitHub Pages): algorithm, KDF, iteration count, salt, IV.

## 4a. Auth, sessions, passwords (full, when the project has accounts or a backend)
- Password storage: bcrypt/argon2/scrypt only; flag plain text, MD5, SHA-*, missing salt.
- Brute-force protection and rate limiting on login and sensitive endpoints.
- Tokens/sessions: lifetime, rotation, logout invalidation, storage place (httpOnly cookie vs localStorage), cookie flags (Secure, HttpOnly, SameSite), CSRF protection.
- Default or hard-coded credentials, admin accounts created on first run.

## 4b. CI/CD (full, when `.github/workflows` or other CI config exists)
- `zizmor .github/workflows` if available, otherwise manual review.
- Secrets printed to logs or passed to untrusted steps; `pull_request_target` with checkout of PR code.
- Third-party actions not pinned to a commit SHA; overly broad `permissions` (prefer read-only by default).
- Script injection via `${{ github.event.* }}` inside `run:` steps.

## 4c. Flutter / mobile (full, when a Flutter/Dart client exists)
- `flutter analyze`; `dart pub outdated`.
- Tokens and passwords: `flutter_secure_storage` (or equivalent), not SharedPreferences or plain files.
- Android: requested permissions, `android:debuggable`, `usesCleartextTraffic`, `allowBackup`, exported components. iOS: `NSAppTransportSecurity` exceptions, Info.plist permissions.
- Hard-coded server URLs/keys; HTTP instead of HTTPS; certificate validation disabled (`badCertificateCallback` returning true).
- Release build obfuscation (`--obfuscate --split-debug-info`) noted as a recommendation.

## 4d. Privacy (full)
- List every external request: analytics, trackers, fonts/CDNs, APIs. Note what data leaves the device and where it goes.
- Personal data collected or stored (names, emails, location, IPs in logs); whether it is necessary.
- For public projects in the EU: cookie/tracking consent needed or not, privacy note present or missing. Describe facts; do not give legal conclusions.

## 4e. Code quality (full)
- Dead code and unused exports/files (`knip` for JS/TS, `vulture` for Python).
- Duplicates (`jscpd`).
- Overly complex functions (`radon cc` for Python, eslint `complexity` rule for JS); list only the worst offenders.
- Test coverage if a coverage tool is already configured.
- Report these as Low unless they hide a real bug.

## 5. Bugs (full; in quick, only obvious ones)
- Run existing tests and linters (`npm test`, `eslint`, `pytest`, `ruff`, `flutter analyze`).
- Three.js leaks: geometry/material/texture never disposed, growing event listeners, objects allocated every frame in the game loop.
- Unhandled errors and promise rejections, races while loading assets, division by zero, NaN in physics, out-of-bounds array access, edge-case input values.
- If the project runs in a browser, open it and check the console for errors.

## 6. Deployed surface (full, only with the user's consent and only their own resources)
- Passive only: security headers (CSP, HSTS, X-Content-Type-Options, Referrer-Policy), HTTPS, exposed files (.git/, .env, backups, source maps containing secrets).
- Server: which services are exposed, default passwords, software versions — only what is visible without attacking. No exploits, brute force or load testing.

## 7. Verification (mandatory in full)
Launch a separate agent that has not seen the search process. Give it only the findings list and access to the code. Its job: confirm or refute each finding, check reachability (does user-controlled data actually reach it), and adjust severity. Remove false positives from the report.

## 8. Report
1. Summary: mode, stack, what was checked and what could not be checked (and why).
2. Findings grouped **Critical / High / Medium / Low**. For each: title, file:line, plain-language explanation, how to reproduce, how to fix (short, with a code example), confidence.
3. What is done well (brief).
4. Recommendation: which items to fix first. Ask which to fix — change nothing without an answer.

quick: report in the chat reply. full: report as a document the user can keep.

## Rules
- Never invent findings: each one is backed by tool output or a specific line of code.
- Never install anything into the project itself and never commit.
- If a tool is unavailable, say so and continue with manual review.
