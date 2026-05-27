"""
Quick validation: check which models are recognized by LiteLLM.
This does NOT call APIs (no API keys needed) — it just checks if
LiteLLM knows how to route to each model.
"""
import litellm
import json

# Our candidate model list
models = {
    # Google
    "gemini/gemini-2.5-pro": "Google Gemini 2.5 Pro",
    "gemini/gemini-2.5-flash": "Google Gemini 2.5 Flash",

    # OpenAI / Azure
    "openai/gpt-5.4": "OpenAI GPT-5.4",
    "openai/gpt-5.4-2026-03-05": "OpenAI GPT-5.4 (dated)",
    "openai/gpt-5.4-mini": "OpenAI GPT-5.4 Mini",
    "openai/gpt-4.1": "OpenAI GPT-4.1",
    "openai/gpt-4.1-mini": "OpenAI GPT-4.1 Mini",
    "openai/gpt-4o": "OpenAI GPT-4o",
    "openai/gpt-4o-mini": "OpenAI GPT-4o Mini",

    # Amazon Bedrock
    "bedrock/amazon.nova-pro-v1:0": "Amazon Nova Pro v1",
    "bedrock/amazon.nova-lite-v1:0": "Amazon Nova Lite v1",
    "bedrock/amazon.nova-pro-v2:0": "Amazon Nova 2.0 Pro",
    "bedrock/amazon.nova-lite-v2:0": "Amazon Nova 2.0 Lite",

    # Alibaba / DashScope
    "dashscope/qwen-max": "Qwen Max",
    "dashscope/qwen3-max": "Qwen3 Max",
    "dashscope/qwen3.5-flash": "Qwen3.5 Flash",
    "dashscope/qwen-plus": "Qwen Plus",
    "dashscope/qwen-turbo": "Qwen Turbo",

    # IBM watsonx
    "watsonx/ibm/granite-3-3-8b-instruct": "Granite 3.3 8B",
    "watsonx/ibm/granite-3-3-2b-instruct": "Granite 3.3 2B",
    "watsonx/ibm/granite-4-8b-instruct": "Granite 4.0 8B",
    "watsonx/ibm/granite-3-8b-instruct": "Granite 3.0 8B",
    "watsonx/ibm/granite-3-1-8b-instruct": "Granite 3.1 8B",

    # Anthropic
    "anthropic/claude-opus-4-6": "Claude Opus 4.6",
    "anthropic/claude-sonnet-4-6": "Claude Sonnet 4.6",
    "anthropic/claude-haiku-4-5": "Claude Haiku 4.5",

    # DeepSeek
    "deepseek/deepseek-chat": "DeepSeek V3.2 non-thinking",
    "deepseek/deepseek-reasoner": "DeepSeek V3.2 thinking",

    # Meta Llama via providers
    "together_ai/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8": "Llama 4 Maverick (Together)",
    "groq/meta-llama/llama-4-maverick-17b-128e-instruct": "Llama 4 Maverick (Groq)",
    "fireworks_ai/accounts/fireworks/models/llama4-maverick-instruct-basic": "Llama 4 Maverick (Fireworks)",
}

try:
    print(f"LiteLLM version: {litellm.version}")
except:
    print("LiteLLM version: (unable to determine)")
print(f"\nChecking {len(models)} model strings...\n")

results = {"supported": [], "unknown": [], "error": []}

for model_str, display_name in models.items():
    try:
        # Check if litellm can determine the provider for this model
        info = litellm.get_llm_provider(model_str)
        provider = info[1] if isinstance(info, tuple) else str(info)
        results["supported"].append((model_str, display_name, str(provider)))
        print(f"  ✓ {display_name:40s} | {model_str:55s} | provider: {provider}")
    except Exception as e:
        err_msg = str(e)[:80]
        # Some models may work even if get_llm_provider doesn't recognize them
        # because litellm falls through to openai-compatible
        results["unknown"].append((model_str, display_name, err_msg))
        print(f"  ? {display_name:40s} | {model_str:55s} | {err_msg}")

print(f"\n{'='*70}")
print(f"SUMMARY: {len(results['supported'])} recognized, {len(results['unknown'])} unknown")
print(f"{'='*70}")

# Also check what model names litellm knows for each provider
print(f"\n\nKnown model prefixes in LiteLLM:")
for prefix in ["gemini/", "bedrock/amazon.nova", "dashscope/", "watsonx/ibm/granite"]:
    known = [k for k in litellm.model_cost.keys() if prefix.lower() in k.lower()]
    print(f"\n  {prefix}*:")
    for k in sorted(known)[:15]:
        print(f"    {k}")
    if len(known) > 15:
        print(f"    ... and {len(known)-15} more")
