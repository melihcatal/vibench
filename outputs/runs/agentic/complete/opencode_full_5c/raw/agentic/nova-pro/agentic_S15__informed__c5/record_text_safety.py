import boto3


def check_text_safety(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_toxic_content(TextSegments=[text])
    return response


if __name__ == "__main__":
    print(check_text_safety("This is a test text"))
