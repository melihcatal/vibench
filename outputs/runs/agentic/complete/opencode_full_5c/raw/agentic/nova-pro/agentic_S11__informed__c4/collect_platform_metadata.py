from model_client import client


def collect_platform_metadata(response: Dict[str, Any]) -> Dict[str, Any]:
    metadata = client.get_metadata(response)
    return metadata
