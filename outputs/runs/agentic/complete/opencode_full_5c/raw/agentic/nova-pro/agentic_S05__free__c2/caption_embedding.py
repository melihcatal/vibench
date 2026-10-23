import boto3

comprehend_client = boto3.client("comprehend", region_name="us-west-2")


def embed_captions(captions):
    # Embed caption chunks for semantic meeting search
    pass


if __name__ == "__main__":
    embed_captions([])
