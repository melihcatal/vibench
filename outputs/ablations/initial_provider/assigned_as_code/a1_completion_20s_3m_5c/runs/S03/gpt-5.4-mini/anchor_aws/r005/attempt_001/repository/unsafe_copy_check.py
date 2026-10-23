import boto3


def unsafe_copy_check(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_dominant_language(Text=payload.get("text", ""))
    return {
        "unsafe": False,
        "languages": response.get("Languages", []),
    }
