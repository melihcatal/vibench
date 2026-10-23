import boto3

transcribe_client = boto3.client("transcribe", region_name="us-west-2")


def stream_chunks():
    # Stream audio chunks from an async source
    pass


if __name__ == "__main__":
    stream_chunks()
