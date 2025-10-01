# Roadmap

This document tracks the evolution of the **AI-Native Template** project toward a full **reference implementation** of AI content monetization standards (e.g. CoMP, RSL, future AP2 extensions).  

---

## v0.1 (MVP)

- [x] Define JSON Schemas:
  - `apifee.schema.json` — pricing/terms manifest  
  - `usage-receipt.schema.json` — signed audit receipts
- [x] CLI tools:
  - `agentapi fees:validate` — validate manifests
  - `agentapi receipts:verify` — verify signed receipts
- [x] Demo adapters:
  - API example (OpenWeather)
  - Static site publisher example (Markdown docs)
- [x] Signed receipts with Ed25519
- [x] CoMP/RSL-compatible well-known manifest (`/.well-known/agent-licensing.json`)
- [x] Robots.txt & HTTP `Link:` headers pointing to manifests
- [x] Basic Cloudflare Worker / NGINX snippet for bot blocking & “402 Payment Required”

---

## v0.2

- [ ] Metering plugins:
  - Token-based
  - Byte-based
  - Request-count
- [ ] SLA and burst-cap fields in fee schema
- [ ] Receipt aggregation (batching multiple calls)
- [ ] Adapter SDKs for Python and Node.js
- [ ] Expanded test coverage and contract tests

---

## v0.3

- [ ] Broker hooks:
  - Export receipts to clearing endpoint
  - Import statements from clearinghouse
- [ ] Dispute-resolution stubs (URLs in manifest + CLI tools)
- [ ] Per-publisher signing keys
- [ ] Analytics event exports for publishers & agents

---

## v1.0

- [ ] Reference “Clearing” API contract:
  - `POST /receipts` for publishers/agents
  - `GET /statements` for reconciliation
- [ ] Multi-protocol adapter (CoMP + RSL + AP2-content mode if ratified)
- [ ] Provenance extensions (C2PA fields in receipts)
- [ ] Production-ready edge enforcement templates

---

## Future Ideas

- UI dashboard for publishers to manage fee menus and view receipts
- Integration with payment providers for real settlement
- Federation hooks for consortium-based clearinghouses

---

**Status Legend:**  
- [x] Completed  
- [ ] Planned / In progress
