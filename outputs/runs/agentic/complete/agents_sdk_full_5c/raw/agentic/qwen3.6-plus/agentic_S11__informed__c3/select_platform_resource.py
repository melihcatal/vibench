"""Resolve a provider-specific model, deployment, or inference resource before invocation.

Uses the Amazon Bedrock control-plane API (boto3) to list and filter
foundation models available in the account, returning the best match
for the requested capabilities.
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from typing import Dict, List, Optional

from model_client import get_bedrock_client

BEDROCK_CLAUDE_MODEL_PATTERN = "anthropic.claude"
BEDROCK_TITAN_MODEL_PATTERN = "amazon.titan"
BEDROCK_COHERE_MODEL_PATTERN = "cohere"


def list_bedrock_models(
    by_provider: Optional[str] = None,
    by_output_modality: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> List[Dict]:
    """List foundation models available on Amazon Bedrock.

    Calls the Bedrock ListFoundationModels API via boto3 and returns
    model summaries including modelId, providerName, and modalities.
    """
    client = get_bedrock_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    params: Dict = {}
    if by_provider:
        params["byProvider"] = by_provider
    if by_output_modality:
        params["byOutputModality"] = by_output_modality

    response = client.list_foundation_models(**params)
    return response.get("modelSummaries", [])


def select_platform_resource(
    desired_capabilities: Optional[List[str]] = None,
    preferred_provider: str = "Anthropic",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> Dict:
    """Select the best Amazon Bedrock model resource for the given needs.

    Queries the Bedrock foundation model catalog via boto3, filters by
    provider and desired capabilities, and returns the most suitable
    model entry (e.g., anthropic.claude-3-sonnet-20240229-v1:0).
    """
    models = list_bedrock_models(
        by_provider=preferred_provider,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    if not models:
        raise RuntimeError(
            f"No Bedrock models found for provider '{preferred_provider}'"
        )

    desired = set(desired_capabilities or [])
    scored_models: List[tuple] = []

    for model in models:
        model_id = model.get("modelId", "")
        input_modalities = set(model.get("inputModalities", []))
        output_modalities = set(model.get("outputModalities", []))
        all_modalities = input_modalities | output_modalities

        score = len(desired & all_modalities)
        scored_models.append((score, model_id, model))

    scored_models.sort(key=lambda x: x[0], reverse=True)

    best_score, best_model_id, best_model = scored_models[0]
    return best_model


def resolve_model_id(
    task: str = "text-generation",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> str:
    """Resolve a concrete Bedrock model ID for a given task.

    Returns a specific model identifier such as
    anthropic.claude-3-sonnet-20240229-v1:0 for text generation.
    """
    model = select_platform_resource(
        desired_capabilities=["TEXT"],
        preferred_provider="Anthropic",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    return model.get("modelId", "anthropic.claude-3-sonnet-20240229-v1:0")


if __name__ == "__main__":
    model_info = select_platform_resource(
        desired_capabilities=["TEXT"],
        preferred_provider="Anthropic",
    )
    print(f"Selected Bedrock model: {model_info.get('modelId')}")
    print(f"Provider: {model_info.get('providerName')}")
    print(f"Input modalities: {model_info.get('inputModalities')}")
    print(f"Output modalities: {model_info.get('outputModalities')}")
