import os


def get_assemblyai_api_key() -> str:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    return api_key


def get_assemblyai_config() -> dict:
    return {
        "api_key": get_assemblyai_api_key(),
        "base_url": os.getenv("ASSEMBLYAI_BASE_URL", "https://api.assemblyai.com"),
    }


def build_headers() -> dict:
    return {
        "authorization": get_assemblyai_api_key(),
        "content-type": "application/json",
    }
