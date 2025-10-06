# Contributing to Kantoberfest Leaderboard

First off, thank you for taking the time to contribute! 🎉 This project powers a community leaderboard that highlights open source contributions during (and beyond) Hacktoberfest. We welcome first‑time contributors and experienced maintainers alike.

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Quick Start (TL;DR)](#quick-start-tldr)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure Overview](#project-structure-overview)
- [Running & Local Development](#running--local-development)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Git / Branch / PR Workflow](#git--branch--pr-workflow)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Checklist](#pull-request-checklist)
- [Issue Reporting & Feature Requests](#issue-reporting--feature-requests)
- [Security](#security)
- [Hacktoberfest Notes](#hacktoberfest-notes)
- [Release & Versioning](#release--versioning)
- [Dependencies](#dependencies)
- [Licensing / Copyright](#licensing--copyright)
- [FAQ](#faq)
- [Community & Code of Conduct](#community--code-of-conduct)

---
## Ways to Contribute

- Bug reports & reproduction cases
- Feature proposals & design discussion
- Improving documentation, examples or onboarding
- Refactoring / performance improvements
- Adding tests & improving reliability
- Helping with issue triage and reviews

## Quick Start (TL;DR)

```bash
# 1. Fork the repo and clone your fork
git clone https://github.com/<you>/kantoberfest-leaderboard.git
cd kantoberfest-leaderboard

# 2. Create & activate a virtualenv
make venv
source .venv/bin/activate   # Windows Git Bash: source .venv/Scripts/activate

# 3. Install deps (incl. dev tools)
make setup

# 4. Copy env file & add your GitHub token
cp .env.example .env
# Edit .env -> add GITHUB_TOKEN (classic or fine-grained w/ repo + read:org scope)

# 5. Run formatting & static checks
make format && make check

# 6. Run locally (Docker build + run)
make run
```

## Development Environment Setup

| Tool | Version (suggested) | Notes |
| ---- | ------------------- | ----- |
| Python | 3.10+ | The project targets modern Python 3. |
| Virtualenv | latest | `make venv` handles creation. |
| Docker (optional runtime) | 24+ | Used by `make run` / container workflow. |
| Git | 2.30+ | Conventional commits encouraged. |

Install dev dependencies via `make setup` which runs an editable install with extras (`.[dev]`).

### Environment Variables

Create `.env` from `.env.example` and populate at least:

- `GITHUB_TOKEN`: Required for GitHub GraphQL API calls.
- Any leaderboard user configuration like `USER_LIST` if applicable.

Never commit secrets. Add new sensitive keys to `.env.example` with placeholder values.

## Project Structure Overview

```text
assets/                 Static web assets (HTML, CSS, JS, images)
leaderboard/            Python package: data fetching + scoring logic
  constants/            Score weights & contribution type enums
  queries/              GraphQL queries
  utils/                Formatting, scoring tables, data helpers
final_html_output.py    Render/assemble final static HTML output
multi_users_fetch.py    Potential multi-user data retrieval script
main.py                 Entry script (if applicable to orchestrate tasks)
Makefile                Common developer commands
Dockerfile              Multi-stage container build (test + main targets)
```

## Running & Local Development

Preferred path:

```bash
make run               # Builds image & runs container mounting current dir
```

Or run natively:

```bash
python final_html_output.py   # or main orchestration script
```
Use `logging` (already set up in modules) rather than ad-hoc prints.

## Coding Standards

- Style: Enforced by `black` (run `make format` or `black .`).
- Static type checking: `pyright` (run `make check`). Add/update type hints when modifying code.
- Imports: Standard library → third-party → local modules.
- Avoid broad `except:` clauses; catch specific exceptions.
- Keep functions cohesive; prefer pure / side-effect-light helpers inside `leaderboard/utils`.
- Document public functions with concise docstrings (Google or reST style acceptable; keep consistent).
- Logging: Use module-level loggers. Avoid logging secrets or large payloads at INFO.

## Testing

We use `pytest`.

```bash
pytest -vv
```

(Or `make venv_test`.)

Add tests when:

- Fixing a bug (add regression test)
- Adding a feature or changing scoring logic
- Modifying complex data transforms (e.g., scoring aggregation)

Test Guidelines:

- Prefer small, deterministic tests
- Use factories / inline fixtures rather than large static JSON
- Avoid network calls: mock GitHub API (e.g., via `responses` or monkeypatching `requests.Session.post`)

## Git / Branch / PR Workflow

1. Create an issue (or pick an existing one labeled `good first issue`, `help wanted`).
2. Branch from `main`: `feat/scoring-weight-adjustment`, `fix/race-condition`, etc.
3. Commit with Conventional Commit messages (see below).
4. Rebase (preferred) or merge `main` before opening PR if branch is stale.
5. Open a Pull Request:
  - Fill in the PR template (if/when added) with summary, motivation, test evidence.
  - Link related issues using `Closes #123` / `Fixes #123`.
6. Address review feedback; keep commits clean (you may squash before merge).
7. A maintainer merges (squash or rebase strategy). Avoid merging your own unreviewed PRs unless trivial docs.

### Branch Naming Examples

- `feat/add-dark-mode`
- `fix/score-normalization`
- `docs/update-readme`
- `refactor/extract-query-builder`

## Commit Message Convention

We follow [Conventional Commits](ConventionalCommits.txt). Core types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Formatting (no code logic change)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding or correcting tests
- `build`: Build system or dependencies
- `ci`: CI configuration
- `chore`: Maintenance tasks

Examples:

```text
feat(scoring): add weight for review comments
fix(fetch): retry on 502 from GitHub API
refactor(utils): simplify score table generation
```

Breaking changes: append `!` or add a `BREAKING CHANGE:` footer.

## Pull Request Checklist

- [ ] Conventional commit title
- [ ] Linked issue(s)
- [ ] Tests added/updated (if logic changed)
- [ ] `make format` run cleanly
- [ ] `make check` (black --check + pyright) passes
- [ ] No secrets in diff
- [ ] Updated docs / README if user-facing change

## Issue Reporting & Feature Requests

When filing an issue include:

- Description & expected vs actual behavior
- Steps to reproduce (commands, environment details)
- Logs (trimmed) or stack trace
- Proposed solution direction (optional)

Labels help triage: `bug`, `enhancement`, `docs`, `good first issue`, `help wanted`.

## Security

If you discover a security vulnerability, DO NOT open a public issue. Instead email: `opensource@yourdomain.example` (Replace with the correct address for the project maintainers). A private disclosure process allows us to patch before public release.

## Hacktoberfest Notes

We welcome Hacktoberfest contributions:

- Focus on meaningful improvements (no spammy formatting-only PRs)
- Look for issues tagged `hacktoberfest` or `good first issue`
- Be patient; maintainers are volunteers

Low-quality / automated PRs may be marked invalid.

## Release & Versioning

While early stage, semantic versioning principles apply:

- `feat` => minor version bump
- `fix` => patch bump
- Breaking changes => major bump

## Dependencies

Runtime deps listed in `setup.py`. Dev deps installed via `.[dev]` extras.
Guidelines:

- Pin versions (already pinned) unless strong reason not to
- Prefer lightweight libs; justify new dependency in PR description
- Remove unused dependencies promptly

## Licensing / Copyright

Project is under the MIT License (see `LICENSE`). By contributing you agree your contributions are licensed under the same terms.

## FAQ

**Q: Do I need to run Docker?**  
A: You can run scripts directly in Python; Docker ensures parity, but it's optional for iteration.

**Q: My GitHub token fails with rate limit?**  
A: Ensure correct scopes and that it's not expired; try a classic PAT with `repo` scope.

**Q: Where do I add a new contribution subtype?**  
A: Update `leaderboard/constants` (types/weights) and adjust any aggregation logic in `leaderboard/utils`.

## Community & Code of Conduct

Participation is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, collaborative, and constructive.

---
Happy hacking! If anything here is unclear, open a `docs` issue or start a discussion.
- Style: Enforced by `black` (run `make format` or `black .`).
- Static type checking: `pyright` (run `make check`). Add/update type hints when modifying code.
- Imports: Standard library → third-party → local modules.
- Avoid broad `except:` clauses; catch specific exceptions.
- Keep functions cohesive; prefer pure / side-effect-light helpers inside `leaderboard/utils`.
- Document public functions with concise docstrings (Google or reST style acceptable; keep consistent).
- Logging: Use module-level loggers. Avoid logging secrets or large payloads at INFO.

## Testing
We use `pytest`.
```bash
$ pytest -vv
```
(Or `make venv_test`.)
Add tests when:
- Fixing a bug (add regression test)
- Adding a feature or changing scoring logic
- Modifying complex data transforms (e.g., scoring aggregation)

Test Guidelines:
- Prefer small, deterministic tests
- Use factories / inline fixtures rather than large static JSON
- Avoid network calls: mock GitHub API (e.g., via `responses` or monkeypatching `requests.Session.post`)

## Git / Branch / PR Workflow
1. Create an issue (or pick an existing one labeled `good first issue`, `help wanted`).
2. Branch from `main`: `feat/scoring-weight-adjustment`, `fix/race-condition`, etc.
3. Commit with Conventional Commit messages (see below).
4. Rebase (preferred) or merge `main` before opening PR if branch is stale.
5. Open a Pull Request:
   - Fill in the PR template (if/when added) with summary, motivation, test evidence.
   - Link related issues using `Closes #123` / `Fixes #123`.
6. Address review feedback; keep commits clean (you may squash before merge).
7. A maintainer merges (squash or rebase strategy). Avoid merging your own unreviewed PRs unless trivial docs.

### Branch Naming Examples
- `feat/add-dark-mode`
- `fix/score-normalization`
- `docs/update-readme`
- `refactor/extract-query-builder`

## Commit Message Convention
We follow [Conventional Commits](ConventionalCommits.txt). Core types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Formatting (no code logic change)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding or correcting tests
- `build`: Build system or dependencies
- `ci`: CI configuration
- `chore`: Maintenance tasks

Examples:
```
feat(scoring): add weight for review comments
fix(fetch): retry on 502 from GitHub API
refactor(utils): simplify score table generation
```
Breaking changes: append `!` or add a `BREAKING CHANGE:` footer.

## Pull Request Checklist
- [ ] Conventional commit title
- [ ] Linked issue(s)
- [ ] Tests added/updated (if logic changed)
- [ ] `make format` run cleanly
- [ ] `make check` (black --check + pyright) passes
- [ ] No secrets in diff
- [ ] Updated docs / README if user-facing change

## Issue Reporting & Feature Requests
When filing an issue include:
- Description & expected vs actual behavior
- Steps to reproduce (commands, environment details)
- Logs (trimmed) or stack trace
- Proposed solution direction (optional)

Labels help triage: `bug`, `enhancement`, `docs`, `good first issue`, `help wanted`.

## Security
If you discover a security vulnerability, DO NOT open a public issue. Instead email: `opensource@yourdomain.example` (Replace with the correct address for the project maintainers). A private disclosure process allows us to patch before public release.

## Hacktoberfest Notes
We welcome Hacktoberfest contributions:
- Focus on meaningful improvements (no spammy formatting-only PRs)
- Look for issues tagged `hacktoberfest` or `good first issue`
- Be patient; maintainers are volunteers

Low-quality / automated PRs may be marked invalid.

## Release & Versioning
While early stage, semantic versioning principles apply:
- `feat` => minor version bump
- `fix` => patch bump
- Breaking changes => major bump

## Dependencies
Runtime deps listed in `setup.py`. Dev deps installed via `.[dev]` extras.
Guidelines:
- Pin versions (already pinned) unless strong reason not to
- Prefer lightweight libs; justify new dependency in PR description
- Remove unused dependencies promptly

## Licensing / Copyright
Project is under the MIT License (see `LICENSE`). By contributing you agree your contributions are licensed under the same terms.

## FAQ
**Q: Do I need to run Docker?**  
A: You can run scripts directly in Python; Docker ensures parity, but it's optional for iteration.

**Q: My GitHub token fails with rate limit?**  
A: Ensure correct scopes and that it's not expired; try a classic PAT with `repo` scope.

**Q: Where do I add a new contribution subtype?**  
A: Update `leaderboard/constants` (types/weights) and adjust any aggregation logic in `leaderboard/utils`.

## Community & Code of Conduct
Participation is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, collaborative, and constructive.

---
Happy hacking! If anything here is unclear, open a `docs` issue or start a discussion.
