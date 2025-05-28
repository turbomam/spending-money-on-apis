import pytest
from spending_money_on_apis.google_maps import GoogleStaticMaps
from spending_money_on_apis.config import load_config

# Load config for tests
load_config()


def test_api_key_required(monkeypatch):
    """Test that API key is required"""
    # Remove the API key from environment
    monkeypatch.delenv("GOOGLE_MAPS_API_KEY", raising=False)

    with pytest.raises(ValueError) as exc_info:
        GoogleStaticMaps()

    assert "GOOGLE_MAPS_API_KEY not found" in str(exc_info.value)


def test_url_generation():
    """Test URL generation"""
    maps = GoogleStaticMaps(api_key="test_key")
    url = maps.get_map_url(center="New York, NY", zoom=10)
    assert "center=New+York%2C+NY" in url
    assert "zoom=10" in url
    assert "key=test_key" in url


def test_config_loading():
    """Test that config can be loaded from local/.env"""
    config_path = load_config()
    assert config_path is not None
