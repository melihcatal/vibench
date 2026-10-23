import os
import boto3

client = boto3.client('bedrock-runtime', region_name='us-west-2')

response = client.invoke_model(
    modelId='amazon.titan-text-express-v1',
    body='{
        "inputText": "Summarize the following error logs:...",
        "textGenerationConfig": {
            "maxTokenCount": 200,
            "temperature": 0.5,
            "topP": 0.9
        }
    }
)
result = response['body'].read()
print(result)