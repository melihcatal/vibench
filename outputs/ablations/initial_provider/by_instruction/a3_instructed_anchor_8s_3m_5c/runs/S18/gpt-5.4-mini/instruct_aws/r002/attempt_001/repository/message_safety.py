import json
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import os


def check_message_safety(payload_text):
    client = ContentSafetyClient(os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"], AzureKeyCredential(os.environ["AZURE_CONTENT_SAFETY_KEY"]))
    result = client.analyze_text(payload_text)
    return {"safe": all(getattr(result, attr, None) is None for attr in ["hate_result", "self_harm_result", "sexual_result", "violence_result"])}


def main():
    payload = json.loads(input())
    print(json.dumps(check_message_safety(payload.get("text", ""))))


if __name__ == "__main__":
    main()
