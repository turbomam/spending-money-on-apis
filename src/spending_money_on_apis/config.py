"""Configuration utilities"""

import os
from pathlib import Path
from dotenv import load_dotenv


def load_config():
    """Load environment variables from local/.env"""
    env_path = Path(__file__).parent.parent.parent / "local" / ".env"
    load_dotenv(env_path)
    return str(env_path)


def get_api_key(key_name: str) -> str:
    """Get an API key from environment"""
    value = os.getenv(key_name)
    if not value:
        raise ValueError(f"{key_name} not found. Please set it in local/.env")
    return value


# Auto-load config when module is imported
load_config()
