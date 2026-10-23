from typing import List

import boto3


def embed_document_sections(sections: List[str], *, region_name: str = None, model_id: str = "amazon.titan-embed-text-v2:0") -> List[list]:
    client = boto3.client("bedrock-runtime", region_name=region_name)
    vectors = []
    for section in sections:
        response = client.invoke_model(modelId=model_id, body=("{"inputText": "" + section.replace('"', '\"') + ""}" ).encode())
        vectors.append(response["body"].read())
    return vectors
