import os
import requests
from typing import List, Dict, Any

def get_doppler_secrets(project: str, config: str) -> List[Dict[str, Any]]:
    """Fetches secrets from the Doppler API."""
    api_key = os.environ.get("DOPPLER_API_KEY")
    if not api_key:
        raise ValueError("DOPPLER_API_KEY environment variable not set.")

    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"project": project, "config": config}
    
    try:
        response = requests.get(
            "https://api.doppler.com/v3/configs/config/secrets",
            headers=headers,
            params=params,
        )
        response.raise_for_status()
        return response.json().get("secrets", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching secrets from Doppler: {e}")
        return []

def rotation_summary(project: str, config: str) -> Dict[str, str]:
    """
    Summarizes secret rotation status by checking for specific keys.
    This is a simplified example; real rotation status would be in metadata.
    """
    secrets = get_doppler_secrets(project, config)
    summary = {}
    for name, data in secrets.items():
        if "computed" in data:
            if "LAST_ROTATED" in data["computed"]:
                summary[name] = f"Rotated at {data['computed']['LAST_ROTATED']}"
            else:
                summary[name] = "Rotation status unknown"
        else:
            summary[name] = "Raw secret, no rotation data."
            
    return summary
