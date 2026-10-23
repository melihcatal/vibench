# collect_platform_metadata.py
# Managed Model Platform Workflow: collect model output with provider metadata
# Provider: Azure OpenAI
import os
import openai

# Configure Azure OpenAI client using environment variables
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-05-15"

def invoke_with_metadata(deployment_name: str, prompt: str) -> dict:
    """Invoke Azure OpenAI model and return both output and usage metadata.

    Args:
        deployment_name: Azure OpenAI deployment identifier.
        prompt: User prompt for generation.

    Returns:
        Dictionary containing 'output' and 'metadata' keys.
    """
    response = openai.ChatCompletion.create(
        deployment=deployment_name,
        messages=[{"role": "user", "content": prompt}],
    )
    # 'usage' contains token counts and model name
    usage = response.usage
    return {
        "output": response.choices[0].message.content,
        "metadata": {
            "model": usage.model,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "deployment_id": deployment_name,
        },
    }

if __name__ == "__main__":
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    prompt_text = "What is the capital of France?"
    result = invoke_with_metadata(deployment, prompt_text)
    print(result)
