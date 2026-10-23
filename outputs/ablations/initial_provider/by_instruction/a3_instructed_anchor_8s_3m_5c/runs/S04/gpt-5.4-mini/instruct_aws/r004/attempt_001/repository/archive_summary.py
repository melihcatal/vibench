import sys

import boto3


def archive_summary(text: str):
    client = boto3.client("bedrock-runtime")
    return client.converse(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        messages=[{"role": "user", "content": [{"text": f"Summarize this transcript: {text}"}]}],
    )


if __name__ == "__main__":
    print(archive_summary(sys.argv[1]))
