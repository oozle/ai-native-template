# AI-Native Template

> **Reference Implementation** for making any API or website **agent-ready**.  
> Implements emerging standards like **CoMP** (AI Content Monetization Protocols), **RSL** (Really Simple Licensing), and is designed to interoperate with future **AP2/APIs** for agentic content.  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Build Status](https://img.shields.io/github/actions/workflow/status/oozle/ai-native-template/ci.yml?branch=main)](https://github.com/oozle/ai-native-template/actions)  
[![Spec Alignment](https://img.shields.io/badge/Spec-CoMP%20%2F%20RSL-blueviolet)](#-standards-alignment)  

---

## ✨ What This Is

AI-Native Template is an **open-source adapter kit** that lets publishers and API providers expose:  

- **Licensing & pricing manifests** in machine-readable form  
- **Signed usage receipts** so agents can prove what they consumed  
- **JSON Schemas** for fee menus and receipts  
- **Schema validators & CLI tools** to reduce friction for developers  
- **Verifier libraries** (Python, TypeScript) for easy integration  
- **Edge enforcement examples** (Cloudflare Worker, NGINX) to block unpaid AI crawlers  
- **Governance scaffolding** (contribution guidelines, security model, spec references)  

This project is not a company product — it’s a **community reference implementation** intended to accelerate adoption of AI-native compensation standards.  

---

## 🚀 Quickstart

Fetch the live manifest:

```bash
curl https://oozle.github.io/ai-native-template/.well-known/agent-licensing.json
```

Validate it against schema:

```bash
ajv validate -s schemas/apifee.schema.json -d apifee.json
```

Verify a signed receipt (example):

```bash
agentapi receipts:verify examples/receipt.example.json keys/publisher.pub
```

---

## 📜 Standards Alignment

| Concept                        | Implemented As                          |
|--------------------------------|-----------------------------------------|
| **Licensing Manifest**         | `/.well-known/agent-licensing.json`      |
| **Pricing Surface**            | `apifee.json` + `schemas/apifee.schema.json` |
| **Usage Receipts**             | `X-Usage-Receipt` header (signed, JSON schema in `schemas/usage-receipt.schema.json`) |
| **Edge Enforcement**           | Cloudflare Worker (`examples/cloudflare-worker.js`), NGINX snippet |
| **Training vs Inference Flags**| `permissions.training / inference` in manifest |
| **Dispute Handling**           | `disputes.url` + `disputes.email`        |
| **Provenance (future)**        | planned C2PA-style receipt extensions   |

---

## 📂 Repo Structure

```
ai-native-template/
├── docs/
│   └── .well-known/
│       └── agent-licensing.json   # Live manifest (GitHub Pages)
├── schemas/
│   ├── apifee.schema.json         # Fee menu schema
│   └── usage-receipt.schema.json  # Receipt schema
├── cli/
│   └── agentapi                   # CLI validator & verifier
├── packages/
│   ├── receipt-verifier-ts/       # TypeScript verifier
│   └── receipt-verifier-py/       # Python verifier
├── examples/
│   ├── openweather_adapter/       # API adapter demo
│   ├── static_site_publisher/     # Markdown static site demo
│   ├── cloudflare-worker.js       # Edge enforcement
│   └── nginx.conf                 # NGINX snippet
├── tests/                         # Pytest-based validation
├── ROADMAP.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CODEOWNERS
├── SPEC-REFERENCES.md
└── LICENSE
```

---

## 🧾 Usage Receipts

Every response can include an `X-Usage-Receipt` header:

```http
X-Usage-Receipt: eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...
```

### Receipt Schema (simplified)

```json
{
  "request_id": "req_01HZZ5A3H3QJCPX4",
  "publisher_id": "urn:publisher:oozle.ai-native-template",
  "resource_id": "kb/article/42",
  "units": { "unit": "1k_tokens", "value": 1.7 },
  "fee_computed": 0.0017,
  "ts": "2025-09-30T22:15:00Z",
  "alg": "Ed25519",
  "signature": "BASE64_SIGNATURE"
}
```

Agents can verify receipts using the CLI or the provided verifier libraries.  

---

## 🛡️ Edge Enforcement

Block AI crawlers unless they present valid receipts.

### Cloudflare Worker

```js
export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname.startsWith('/api/')) {
      const receipt = request.headers.get('X-Usage-Receipt');
      if (!receipt) {
        return new Response(JSON.stringify({
          error: "Payment required",
          manifest: "https://oozle.github.io/ai-native-template/.well-known/agent-licensing.json"
        }), { status: 402, headers: { "content-type": "application/json" }});
      }
    }
    return fetch(request);
  }
};
```

### NGINX Snippet

```nginx
location /api/ {
  if ($http_x_usage_receipt = "") {
    return 402 '{"error":"Payment required","manifest":"https://oozle.github.io/ai-native-template/.well-known/agent-licensing.json"}';
  }
  proxy_pass http://origin_upstream;
}
```

---

## 🛣️ Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed milestones.  

Highlights:  
- **v0.1 (MVP):** Schemas, receipts, manifest, edge enforcement  
- **v0.2:** Metering plugins, SDKs, batch receipts  
- **v0.3:** Clearing hooks, dispute stubs, per-publisher keys  
- **v1.0:** Full clearing API, multi-protocol adapter, provenance extensions  

---

## 📈 Governance & Specs

- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute  
- [SECURITY.md](SECURITY.md) — threat model & reporting  
- [CODEOWNERS](CODEOWNERS) — repo ownership  
- [SPEC-REFERENCES.md](SPEC-REFERENCES.md) — CoMP, RSL, Cloudflare, C2PA links  
- [ADOPTERS.md](ADOPTERS.md) — for projects using this template  

---

## 🔮 Vision

The web is shifting from **attention/ads → transaction/licensing**.  
AI agents consume content at scale — publishers need **transparent compensation**.  

This OSS project aims to:  
1. Lower the barrier for publishers to expose terms and pricing.  
2. Provide agents with verifiable receipts and predictable costs.  
3. Enable clearinghouses and mediators to reconcile usage fairly.  

---

## 📬 Contact

Maintainer: [GitHub @oozle](https://github.com/oozle)  
Live Manifest: [agent-licensing.json](https://oozle.github.io/ai-native-template/.well-known/agent-licensing.json)  

---
