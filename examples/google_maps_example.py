#!/usr/bin/env python3
from pathlib import Path
from dotenv import load_dotenv
from spending_money_on_apis.google_maps import GoogleStaticMaps

# Load environment variables from local/.env
env_path = Path(__file__).parent.parent / "local" / ".env"
load_dotenv(env_path)


def main():
    # Initialize client
    maps = GoogleStaticMaps()

    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Example 1: Simple map
    maps.get_map(
        center="Times Square, New York, NY",
        zoom=15,
        save_as=output_dir / "times_square.png",
    )
    print("✓ Saved Times Square map")

    # Example 2: Map with markers
    maps.get_map(
        center="San Francisco, CA",
        zoom=12,
        markers=[
            {
                "color": "red",
                "label": "G",
                "location": "Golden Gate Bridge, San Francisco, CA",
            },
            {
                "color": "blue",
                "label": "A",
                "location": "Alcatraz Island, San Francisco, CA",
            },
        ],
        save_as=output_dir / "sf_landmarks.png",
    )
    print("✓ Saved San Francisco landmarks map")


if __name__ == "__main__":
    main()
