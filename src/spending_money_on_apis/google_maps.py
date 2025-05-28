import requests
from pathlib import Path
from urllib.parse import urlencode
from typing import Optional, List, Dict, Union
from .config import load_config, get_api_key

# Load config on module import
load_config()


class GoogleStaticMaps:
    """Client for Google Static Maps API"""

    def __init__(self, api_key: Optional[str] = None):
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = get_api_key("GOOGLE_MAPS_API_KEY")
        self.base_url = "https://maps.googleapis.com/maps/api/staticmap"

    def get_map(
        self,
        center: Optional[str] = None,
        zoom: int = 13,
        size: str = "600x400",
        maptype: str = "roadmap",
        markers: Optional[List[Dict[str, str]]] = None,
        path: Optional[str] = None,
        save_as: Optional[Union[str, Path]] = None,
    ) -> Union[bytes, bool]:
        """Fetch a static map from Google Maps API"""

        params = {"key": self.api_key, "size": size, "maptype": maptype, "zoom": zoom}

        if center:
            params["center"] = center

        if markers:
            marker_strings = []
            for marker in markers:
                marker_parts = []
                for key in ["color", "label", "size"]:
                    if key in marker:
                        marker_parts.append(f"{key}:{marker[key]}")
                if "location" in marker:
                    marker_parts.append(marker["location"])
                marker_strings.append("|".join(marker_parts))
            params["markers"] = marker_strings

        if path:
            params["path"] = path

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()

        if save_as:
            save_path = Path(save_as)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(response.content)
            return True

        return response.content

    def get_map_url(self, **kwargs) -> str:
        """Generate a URL for a static map"""
        params = {k: v for k, v in kwargs.items() if v is not None}
        params["key"] = self.api_key
        return f"{self.base_url}?{urlencode(params)}"
