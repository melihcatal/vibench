import os
from openai import OpenAI

def select_platform_resource(model_alias: str) -> str:
    # In a more complex scenario, this would map an alias to a specific deployment ID or fine-tuned model.
    # For OpenAI, the model_alias can directly be the model name.
    if model_alias == "default_chat":
        return "gpt-4o"
    elif model_alias == "fast_chat":
        return "gpt-3.5-turbo"
    else:
        return model_alias
