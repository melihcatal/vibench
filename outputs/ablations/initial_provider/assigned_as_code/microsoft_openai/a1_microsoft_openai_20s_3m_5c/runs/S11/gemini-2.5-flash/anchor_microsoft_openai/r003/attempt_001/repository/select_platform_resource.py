import os

def select_platform_resource(model_name: str, config: dict = None) -> str:
    config = config or {}
    # In a real scenario, this would involve listing available deployments
    # or validating the model_name against existing resources.
    # For this example, we assume the model_name is the deployment ID.
    # You could have a mapping or check an environment variable for default.
    deployment_id = config.get("AZURE_OPENAI_DEPLOYMENT_ID") or os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")
    if deployment_id and model_name == deployment_id:
        return deployment_id
    elif not deployment_id:
        # If no default deployment ID is set, we just use the provided model_name
        return model_name
    else:
        # This part could be expanded for more complex resource selection logic
        print(f"Warning: Requested model_name '{model_name}' does not match default deployment ID '{deployment_id}'. Using '{model_name}'.")
        return model_name
