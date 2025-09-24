# Contributing

1. Fork and branch from `main`.
2. Add/modify adapters under `providers/<name>/adapter`.
3. **Every new route must have a fee entry** in `pricing/apifee.json`.
4. Ensure receipts are emitted and tests pass.
5. Run `pytest` locally and `agentapi fees:validate` before opening a PR.
6. CI must be green.
