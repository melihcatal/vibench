import boto3

transcribe_client = boto3.client("transcribe", region_name="us-west-2")


def stream_with_language():
    # Start a streaming recognizer with language and punctuation settings
    pass


if __name__ == "__main__":
    stream_with_language()
