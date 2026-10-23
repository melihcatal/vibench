import json
from model_client import ManagedModelClient


def collect_metadata(project_id, deployment_id, payload):
    client = ManagedModelClient(project_id=project_id, deployment_id=deployment_id)
    response = client.invoke(payload)
    # Collect provider metadata alongside output
    result = {
        "output": response.get("output"),
        "provider": "openai",  # identifiable provider
        "usage": response.get("usage"),
        "resource_id": response.get("resource_id"),
    }
    return result


if __name__ == "__main__":
    payload = json.load(sys.stdin)
    result = collect_metadata("my-project", "my-deployment", payload)
    print(json.dumps(result, indent=2))
