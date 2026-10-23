import boto3

transcribe_client = boto3.client("transcribe", region_name="us-west-2")


def stream_microphone():
    # Stream microphone audio and yield interim transcripts
    pass


if __name__ == "__main__":
    stream_microphone()
