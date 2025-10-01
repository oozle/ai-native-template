# AI-Native Template

> **Reference Implementation** for making any API or website **agent-ready**.  
> Implements emerging standards like **CoMP** (AI Content Monetization Protocols), **RSL** (Really Simple Licensing), and is designed to interoperate with future **AP2/APIs** for agentic content.  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Build Status](https://img.shields.io/github/actions/workflow/status/oozle/ai-native-template/ci.yml?branch=main)](https://github.com/oozle/ai-native-template/actions)  
[![Spec Alignment](https://img.shields.io/badge/Spec-CoMP%20%2F%20RSL-blueviolet)](#standards-alignment)  

---

## ✨ What This Is

AI-Native Template is an **open-source adapter kit** that lets publishers and API providers expose:  

- **Licensing & pricing manifests** in machine-readable form  
- **Signed usage receipts** so agents can prove what they consumed  
- **Schema validators & CLI tools** to reduce friction for developers  
- **Edge enforcement examples** (e.g. Cloudflare Worker, NGINX) to block unpaid AI crawlers  
- **OSS reference implementation** aligned with the **IAB Tech Lab CoMP working group**  

This project is not a company product — it’s a **community reference implementation** intended to accelerate adoption of AI-native compensation standards.  

---

## 🚀 Quickstart

Fetch the demo manifest:

```bash
curl https://oozle.github.io/ai-native-template/.well-known/agent-licensing.json
```

Validate it with the CLI:

```bash
agentapi fees:validate docs/.well-known/agent-licensing.json
```

Verify a signed receipt (example header file):

```bash
agentapi receipts:verify examples/receipt.txt keys/publisher.pub
```

---

## 📜 Standards Alignment

| Concept                        | Implemented As                          |
|--------------------------------|-----------------------------------------|
| **Licensing Manifest**         | `/.well-known/agent-licensing.json`      |
| **Pricing Surface**            | `apifee.json` + `apifee.schema.json`    |
| **Usage Receipts**             | `X-Usage-Receipt` header (signed)        |
| **Edge Enforcement**           | Cloudflare Worker & NGINX examples      |
| **Training vs Inference Flags**| `permissions.training / inference`       |
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
│   ├── apifee.schema.json
│   └── usage-receipt.schema.json
├── cli/
│   └── agentapi                   # CLI validator & verifier
├── examples/
│   ├── openweather_adapter/       # API adapter demo
│   └── static_site_publisher/     # Markdown static site demo
├── tests/                         # Pytest-based validation
├── ROADMAP.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## 🧾 Usage Receipts

Every response can include an `X-Usage-Receipt` header:

```http
X-Usage-Receipt: eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...
```

Receipts contain:

- `request_id` (unique nonce)  
- `publisher_id`  
- `resource_id`  
- `units` consumed (tokens, bytes, requests)  
- `fee_computed`  
- `ts` timestamp  
- `signature` (Ed25519)  

Agents can verify receipts using the CLI or a lightweight library.  

---

## 🛡️ Edge Enforcement

Example: block AI crawlers unless they present valid receipts.

### Cloudflare Worker

```js
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith('/api/')) {
      if (!request.headers.get("X-Usage-Receipt")) {
        return new Response(
          JSON.stringify({
            error: "Payment required",
            manifest: "https://oozle.github.io/ai-native-template/.well-known/agent-licensing.json"
          }),
          { status: 402, headers: { "Content-Type": "application/json" } }
        );
      }
    }
    return fetch(request);
  }
};
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

## 🤝 Contributing

We welcome contributions!  

- Open issues or PRs for schema feedback, new adapters, or enforcement examples.  
- Add yourself to `ADOPTERS.md` if you integrate this template into a project.  
- Follow our [CONTRIBUTING.md](CONTRIBUTING.md) guidelines.  

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
