import json
from storage_client import get_bedrock_runtime_client


def summarize_text(text_content: str) -> dict:
    """
    Summarizes text content using Amazon Titan Text G1 - Express via Bedrock.
    """
    bedrock_client = get_bedrock_runtime_client()

    model_id = "amazon.titan-text-express-v1"

    prompt = (
        f"Please provide a concise summary of the following text:\n\n{text_content}"
    )

    body = json.dumps(
        {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "stopSequences": [],
                "temperature": 0.7,
                "topP": 0.9,
            },
        }
    )

    try:
        response = bedrock_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        summary = response_body.get("results")[0].get("outputText")

        return {"status": "success", "summary": summary.strip()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
