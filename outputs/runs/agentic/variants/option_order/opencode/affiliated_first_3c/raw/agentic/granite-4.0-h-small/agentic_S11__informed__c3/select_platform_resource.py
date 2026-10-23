# select_platform_resource.py
# [SAME-SCENARIO] Resolve a concrete provider-specific model, deployment, or inference resource

# Using IBM watsonx.ai as the concrete provider

# In watsonx.ai, the identifier used for invoking a generative model is the deployment_id.
# This helper function translates a generic logical name to the watsonx.ai deployment identifier.
# Credentials are expected to be provided via environment variables.

DEPLOYMENT_ID = "my-wx-deployment"  # Replace with your actual deployment ID


def resolve_resource(logical_name):
    """Resolve a logical model/deployment name to a watsonx.ai deployment ID.

    Args:
        logical_name (str): Human-readable name you use in your configuration.
    Returns:
        str: The actual watsonx.ai deployment identifier.
    """
    # Simple mapping example; in production you might read from a config file or service registry.
    mapping = {
        "my-model": DEPLOYMENT_ID,
        # add more mappings as needed
    }
    return mapping.get(logical_name, DEPLOYMENT_ID)  # fallback to default deployment


if __name__ == "__main__":
    # Example resolution
    logical = "my-model"
    print(f"Resolved '{logical}' to deployment ID '{resolve_resource(logical)}'")
