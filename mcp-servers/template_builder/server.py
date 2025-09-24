import json, os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Tiny MCP-ish HTTP shim for demo purposes; in real use you'd run a proper MCP server framework.
# Exposes two JSON endpoints: /scaffold_adapter and /validate_fee_menu

def scaffold_adapter(name: str, upstream_base_url: str):
    base = f"providers/{name}/adapter"
    os.makedirs(f"{base}/pricing", exist_ok=True)
    os.makedirs(f"{base}/hooks", exist_ok=True)
    os.makedirs(f"{base}/tests", exist_ok=True)
    fee_path = f"{base}/pricing/apifee.json"
    if not os.path.exists(fee_path):
        with open(fee_path, "w") as f:
            json.dump({
              "provider": name, "version": "1.0.0", "currency": "USD",
              "plans": [{"id":"dev","displayName":"Developer","billing":{"type":"credit","minPurchase":50},"rates":[]}],
              "sla":{"p99LatencyMs":1000,"uptimePct":99.0}
            }, f, indent=2)
    return {"ok": True, "path": base, "upstream_base_url": upstream_base_url}

def validate_fee_menu(path: str):
    with open(path) as f:
        j = json.load(f)
    missing = [k for k in ["provider","currency","plans"] if k not in j]
    return {"valid": len(missing)==0, "missing": missing}

class H(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode())

    # NEW: health + capabilities
    def do_GET(self):
        if self.path == "/":
            return self._json(200, {
                "ok": True,
                "name": "Template Builder (demo)",
                "capabilities": ["/scaffold_adapter", "/validate_fee_menu"]
            })
        return self._json(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length","0"))
        body = json.loads(self.rfile.read(length) or "{}")
        if self.path == "/scaffold_adapter":
            res = scaffold_adapter(body.get("name","new-provider"), body.get("upstream_base_url",""))
            return self._json(200, res)
        if self.path == "/validate_fee_menu":
            res = validate_fee_menu(body.get("path","providers/demo-openweather/adapter/pricing/apifee.json"))
            return self._json(200, res)
        return self._json(404, {"error":"not found"})

if __name__ == "__main__":
    port = int(os.getenv("PORT","3845"))
    print(f"Template Builder MCP demo listening on http://127.0.0.1:{port}")
    HTTPServer(("127.0.0.1", port), H).serve_forever()
