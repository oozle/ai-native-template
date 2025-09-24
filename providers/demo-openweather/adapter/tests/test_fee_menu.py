import json
from app import APP

def test_all_routes_have_fee_entries():
    with open("pricing/apifee.json") as f:
        menu = json.load(f)
    resources = {r["resource"] for plan in menu["plans"] for r in plan["rates"]}
    for route in APP.routes:
        # Only check our public weather routes
        if getattr(route, "path", "").startswith("/weather/"):
            # Convert `/weather/current` -> `weather.current.get`
            normalized = route.path.strip("/").replace("/", ".") + ".get"
            assert normalized in resources, f"Missing fee entry for {normalized}"
