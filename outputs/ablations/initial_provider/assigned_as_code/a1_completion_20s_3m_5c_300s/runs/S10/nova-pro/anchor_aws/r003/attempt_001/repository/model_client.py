import boto3


def get_bedrock_client(region=None):
    return boto3.client("bedrock-runtime", region_name=region)


def prepare_payload(prompt, model_id="amazon.nova-pro-v1:0"):
    return {
        "modelId": model_id,
        "messages": [{
            "role": "user",
            "content": [{
                "text": prompt
            }]
        }]
    }


def parse_response(response):
    return "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)