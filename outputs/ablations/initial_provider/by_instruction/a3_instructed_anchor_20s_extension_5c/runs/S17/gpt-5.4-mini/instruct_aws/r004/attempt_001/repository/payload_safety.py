import boto3

from security_client import load_security_client_config


def payload_safety(payload: str) -> dict:
    comprehend = boto3.client("comprehend", region_name=load_security_client_config().region_name)
    return comprehend.detect_dominant_language(Text=payload)


def main() -> None:
    payload_safety("sample plaintext")


if __name__ == "__main__":
    main()
