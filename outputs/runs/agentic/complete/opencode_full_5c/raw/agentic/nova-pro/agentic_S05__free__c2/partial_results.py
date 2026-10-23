import boto3

transcribe_client = boto3.client("transcribe", region_name="us-west-2")


def handle_partial_results():
    # Handle partial and final streaming recognition events
    pass


if __name__ == "__main__":
    handle_partial_results()
