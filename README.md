# AI-Native API Template (OSS Core)

Minimal open-source template to make any API "agent-ready":
- **Normalized schema** (OpenAPI)
- **Usage-fee menu** (`apifee.json`) for transparent pricing
- **Metering + signed receipts** (`X-Usage-Receipt` headers)
- **Tests/CI guardrails** (no route ships without a price)
- Optional **MCP/Workflows** for Warp

## Quick Start (local)
```bash
cd providers/demo-openweather/adapter
python -m pip install fastapi uvicorn httpx pytest
uvicorn app:APP --reload
```
```bash
curl -i "http://127.0.0.1:8000/weather/current?lat=37.77&lon=-122.42"
```

## Fee Menu
See `providers/demo-openweather/adapter/pricing/apifee.json`.

## Tests
```bash
cd providers/demo-openweather/adapter
pytest -q
```

## CLI (`agentapi`)
```bash
cd cli && npm install && npm link
agentapi fees:validate providers/demo-openweather/adapter/pricing/apifee.json
```

## License
MIT
