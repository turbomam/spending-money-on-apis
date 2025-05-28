#!/usr/bin/env python3
"""Test configuration loading"""
import os
from pathlib import Path
from spending_money_on_apis.config import load_config


def main():
    print("Testing configuration loading...\n")

    # Load configuration
    config_path = load_config()
    print(f"✓ Loaded configuration from: {config_path}")

    # Check for API keys
    api_keys = [
        "GOOGLE_MAPS_API_KEY",
        # Add other API keys you use
    ]

    print("\nChecking API keys:")
    for key_name in api_keys:
        try:
            key_value = os.getenv(key_name)
            if key_value:
                print(f"✓ {key_name}: {key_value[:10]}...")
            else:
                print(f"✗ {key_name}: Not found")
        except Exception as e:
            print(f"✗ {key_name}: Error - {e}")

    # Show all paths checked
    print("\nPaths checked for local/.env:")
    possible_paths = [
        Path.cwd() / "local" / ".env",
        Path(__file__).parent / "local" / ".env",
        Path.home() / "gitrepos" / "spending-money-on-apis" / "local" / ".env",
    ]

    for path in possible_paths:
        exists = "✓ EXISTS" if path.exists() else "✗ Not found"
        print(f"{exists}: {path}")


if __name__ == "__main__":
    main()
