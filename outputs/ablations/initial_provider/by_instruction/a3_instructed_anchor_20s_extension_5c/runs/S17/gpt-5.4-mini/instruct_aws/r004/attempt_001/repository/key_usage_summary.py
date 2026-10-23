import boto3

from security_client import load_security_client_config


def key_usage_summary() -> dict:
    config = load_security_client_config()
    cloudtrail = boto3.client("cloudtrail", region_name=config.region_name)
    return cloudtrail.lookup_events(LookupAttributes=[{"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"}])


def main() -> None:
    key_usage_summary()


if __name__ == "__main__":
    main()
