import boto3
import os

client = boto3.client(
    "bedrock-runtime",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def summarize_logs(log_events):
    response = client.invoke_model(
        modelId="amazon.titan-text-express-v1",
        body=json.dumps(
            {
                "inputText": "\n".join(log_events),
                "textGenerationConfig": {
                    "maxTokenCount": 200,
                    "temperature": 0.5,
                    "topP": 0.9,
                },
            }
        ),
    )
    result = json.loads(response["body"].read())
    return result["results"][0]["outputText"]


log_events = [
    "ERROR: Failed to connect to database",
    "ERROR: User authentication failed",
    "ERROR: Service unavailable",
]

summary = summarize_logs(log_events)
print(summary)
