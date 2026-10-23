import boto3
import json

def answer_with_context(question: str, context: str) -> str:
    """
    Calls AWS Bedrock to answer a question using provided context.
    """
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
    )

    prompt = f"""Human: Answer the following question based on the provided context.
<context>
{context}
</context>
<question>
{question}
</question>
Assistant:"""

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.3,
        "top_p": 0.9
    })

    model_id = "anthropic.claude-v2"
    content_type = "application/json"
    accept = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
        contentType=content_type,
        accept=accept
    )

    response_body = json.loads(response.get("body").read())
    return response_body.get("completion")

