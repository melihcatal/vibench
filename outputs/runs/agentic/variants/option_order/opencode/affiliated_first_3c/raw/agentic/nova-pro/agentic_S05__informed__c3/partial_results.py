import boto3
import os

transcribe_client = boto3.client(
    "transcribe",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def handle_recognition_events(events):
    for event in events:
        if "TranscriptResultStream" in event:
            for result in event["TranscriptResultStream"]:
                if "Results" in result:
                    for item in result["Results"]:
                        if "Alternatives" in item:
                            for alternative in item["Alternatives"]:
                                print(alternative["Transcript"])
