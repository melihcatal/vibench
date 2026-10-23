import os
import json
from model_client import ManagedModelClient


def invoke_model(project_id, deployment_id, payload):
    client = ManagedModelClient(project_id=project_id, deployment_id=deployment_id)
    response = client.invoke(payload)
    # Provider-specific identifiable call
    print(f"Calling OpenAI GPT-4o (provider: openai)")
    return response


if __name__ == "__main__":
    # Example usage: read payload from stdin
    payload = json.load(sys.stdin)
    result = invoke_model("my-project", "my-deployment", payload)
    print(json.dumps(result, indent=2))
