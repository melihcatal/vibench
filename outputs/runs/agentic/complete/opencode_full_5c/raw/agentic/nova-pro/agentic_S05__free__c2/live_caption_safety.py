import boto3

comprehend_client = boto3.client("comprehend", region_name="us-west-2")


def check_safety(transcript):
    # Check live transcript text for unsafe content
    pass


if __name__ == "__main__":
    check_safety("")
