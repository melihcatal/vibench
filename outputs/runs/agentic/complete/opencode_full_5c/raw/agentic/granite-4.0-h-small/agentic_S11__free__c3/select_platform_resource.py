import json
from model_client import ManagedModelClient


def select_resource(project_id=None, deployment_id=None, model_id=None):
    # Resolve provider-specific resource identifiers
    if not model_id:
        # Default to OpenAI's gpt-4o model
        model_id = "gpt-4o"
    # Provider identifiable selection
    print(f"Selected OpenAI model: {model_id} (provider: openai)")
    return {
        "model_id": model_id,
        "deployment_id": deployment_id or model_id,
    }


if __name__ == "__main__":
    args = json.load(sys.stdin)
    print(json.dumps(select_resource(**args), indent=2))
