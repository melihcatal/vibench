import boto3

translate_client = boto3.client("translate", region_name="us-west-2")


def translate_captions(captions):
    # Translate live captions into another language
    pass


if __name__ == "__main__":
    translate_captions([])
