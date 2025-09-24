import pytest
import json
from fastapi.testclient import TestClient
from app import APP


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(APP)


def test_current_weather_parameter_validation(client):
    """Test parameter validation for the weather endpoint."""
    # Test missing lat parameter
    response = client.get("/weather/current?lon=-122.42")
    assert response.status_code == 422
    
    # Test missing lon parameter  
    response = client.get("/weather/current?lat=37.77")
    assert response.status_code == 422
    
    # Test missing both parameters
    response = client.get("/weather/current")
    assert response.status_code == 422


def test_current_weather_invalid_parameters(client):
    """Test weather request with invalid parameter types."""
    # Test invalid lat
    response = client.get("/weather/current?lat=invalid&lon=-122.42")
    assert response.status_code == 422
    
    # Test invalid lon
    response = client.get("/weather/current?lat=37.77&lon=invalid")
    assert response.status_code == 422


def test_usage_tracking_headers_present(client):
    """Test that usage tracking headers are present even when upstream fails."""
    # This will fail to connect to the upstream API, but should still have headers
    response = client.get("/weather/current?lat=37.77&lon=-122.42")
    
    # Even if the request fails, middleware should add usage headers
    assert "X-Usage-Receipt" in response.headers
    assert "X-Usage-Receipt-Body" in response.headers
    
    # Parse and validate usage receipt structure
    receipt_body = json.loads(response.headers["X-Usage-Receipt-Body"])
    assert "resource" in receipt_body
    assert "status_code" in receipt_body
    assert "duration_ms" in receipt_body  
    assert "price" in receipt_body
    assert "ts" in receipt_body
    assert receipt_body["resource"] == "get:/weather/current"


def test_different_endpoints_different_prices(client):
    """Test that different endpoints have different prices in receipts."""
    # Test current weather endpoint
    response_current = client.get("/weather/current?lat=37.77&lon=-122.42")
    receipt_current = json.loads(response_current.headers["X-Usage-Receipt-Body"])
    
    # Test forecast endpoint
    response_forecast = client.get("/weather/forecast?lat=37.77&lon=-122.42")
    receipt_forecast = json.loads(response_forecast.headers["X-Usage-Receipt-Body"])
    
    # Verify different prices
    assert receipt_current["price"] == 0.002
    assert receipt_forecast["price"] == 0.004
    
    # Verify correct resource names
    assert receipt_current["resource"] == "get:/weather/current"
    assert receipt_forecast["resource"] == "get:/weather/forecast"


def test_usage_receipt_signature_format(client):
    """Test that usage receipt signature is a valid hex string."""
    response = client.get("/weather/current?lat=37.77&lon=-122.42")
    
    receipt_signature = response.headers["X-Usage-Receipt"]
    
    # Check that signature is a hex string (64 chars for SHA256)
    assert len(receipt_signature) == 64
    assert all(c in '0123456789abcdef' for c in receipt_signature.lower())