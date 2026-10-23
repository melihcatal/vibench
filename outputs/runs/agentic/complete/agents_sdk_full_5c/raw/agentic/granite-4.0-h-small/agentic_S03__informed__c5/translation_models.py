import os
import json

def load_config(file_path: str = 'config.json') -> dict:
    """Utility to load JSON config, falling back to env vars.",
    try:
        with open(file_path, 'r') as fp:
            return json.load(fp)
    except Exception:
        return {
            'WATSONX_API_KEY': os.getenv('WATSONX_API_KEY'),
            'WATSONX_PROJECT_ID': os.getenv('WATSONX_PROJECT_ID')
        }
