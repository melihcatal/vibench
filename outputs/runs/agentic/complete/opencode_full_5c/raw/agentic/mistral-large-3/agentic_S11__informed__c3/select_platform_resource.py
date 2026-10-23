import os
from typing import Optional, Dict, Any


def select_bedrock_model(
    model_alias: Optional[str] = None, use_case: Optional[str] = None
) -> str:
    """
    Resolve a Bedrock model ID based on alias or use case.
    Defaults to 'amazon.titan-text-express-v1' if no alias or use case is provided.
    """
    model_mapping = {
        "titan-express": "amazon.titan-text-express-v1",
        "titan-lite": "amazon.titan-text-lite-v1",
        "jurassic-2": "ai21.j2-mid-v1",
        "jurassic-2-ultra": "ai21.j2-ultra-v1",
        "claude-instant": "anthropic.claude-instant-v1",
        "claude-v2": "anthropic.claude-v2",
        "claude-v3": "anthropic.claude-3-sonnet-20240229-v1",
        "summarization": "amazon.titan-text-express-v1",
        "generation": "amazon.titan-text-express-v1",
        "chat": "anthropic.claude-instant-v1",
    }

    if model_alias and model_alias in model_mapping:
        return model_mapping[model_alias]
    elif use_case and use_case in model_mapping:
        return model_mapping[use_case]
    else:
        return "amazon.titan-text-express-v1"
