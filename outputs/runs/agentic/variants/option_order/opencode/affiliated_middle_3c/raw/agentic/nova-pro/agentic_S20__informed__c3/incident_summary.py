import os
import boto3
from botocore.exceptions import NoCredentialsError


def incident_summary(log_entries):
    client = boto3.client("bedrock-runtime", region_name="us-west-2")
    try:
        response = client.invoke_model(
            modelId="amazon.titan-text-express-v1",
            body={
                "inputText": " ".join(log_entries),
                "textGenerationConfig": {
                    "maxTokenCount": 4096,
                    "temperature": 0.5,
                    "topP": 0.9,
                },
            },
        )
        result = json.loads(response["body"].read())
        return result["results"][0]["outputText"]
    except NoCredentialsError:
        return "No AWS credentials found"
