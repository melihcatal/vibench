import os
import boto3


def unsafe_copy_check(text):
    comprehend = boto3.client(
        "comprehend",
        region_name="us-west-2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    result = comprehend.detect_toxic_content(Text=text, LanguageCode="en")
    return result["ToxicContentDetected"]


if __name__ == "__main__":
    print(unsafe_copy_check("This is a toxic comment."))
