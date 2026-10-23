# select_platform_resource.py
# Managed Model Platform Workflow: resolve a provider-specific model/resource
# Provider: Azure OpenAI
import os

def get_deployment_name() -> str:
    """Retrieve the deployment identifier for the model resource.

    Returns:
        Deployment name configured via environment variable.
    """
    return os.getenv("AZURE_OPENAI_DEPLOYMENT")

if __name__ == "__main__":
    deployment = get_deployment_name()
    print(f"Selected deployment: {deployment}")
