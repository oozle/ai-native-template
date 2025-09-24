from fastapi import FastAPI, Request, Response
import time, json, hmac, hashlib, os
import httpx

APP = FastAPI(title="Demo OpenWeather AI-Native Wrapper", version="1.0.0")
UPSTREAM = "https://api.open-meteo.com/v1"
LEDGER_SECRET = os.getenv("LEDGER_SECRET", "dev-secret")

def sign_receipt(payload: dict) -> str:
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    sig = hmac.new(LEDGER_SECRET.encode(), body.encode(), hashlib.sha256).hexdigest()
    return sig

@APP.middleware("http")
async def meter_requests(request: Request, call_next):
    started = time.time()
    response: Response = await call_next(request)
    duration_ms = int((time.time() - started) * 1000)
    resource = f"{request.method.lower()}:{request.url.path}"
    price_table = {"/weather/current": 0.002, "/weather/forecast": 0.004}
    price = price_table.get(request.url.path, 0.0)
    receipt = {
        "resource": resource,
        "status_code": response.status_code,
        "duration_ms": duration_ms,
        "price": price,
        "ts": int(time.time())
    }
    response.headers["X-Usage-Receipt"] = sign_receipt(receipt)
    response.headers["X-Usage-Receipt-Body"] = json.dumps(receipt)
    return response

@APP.get("/weather/current")
async def current_weather(lat: float, lon: float):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{UPSTREAM}/forecast", params={"latitude":lat,"longitude":lon,"current":"temperature_2m"})
        r.raise_for_status()
        j = r.json()
        return {"temperature_c": j["current"]["temperature_2m"]}

@APP.get("/weather/forecast")
async def forecast(lat: float, lon: float, hours: int = 24):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{UPSTREAM}/forecast", params={"latitude":lat,"longitude":lon,"hourly":"temperature_2m"})
        r.raise_for_status()
        j = r.json()
        return {"hourly_temp_c": j["hourly"]["temperature_2m"][:hours]}
