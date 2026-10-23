# stream_platform_generation.py
# Managed Model Platform Workflow: stream output from a managed model
# Provider: Azure OpenAI
import os
import openai

# Configure Azure OpenAI client using environment variables
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-05-15"

def stream_chat_completion(deployment_name: str, prompt: str) -> openai.ChatCompletionStream:
    """Stream a chat completion from Azure OpenAI.

    Args:
        deployment_name: Name of the deployment.
        prompt: User prompt to generate.

    Returns:
        Async iterator yielding response chunks.
    """
    return openai.ChatCompletion.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

if __name__ == "__main__":
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    prompt = "Explain how photosynthesis works, but in a poetic style."
    print(f"Streaming response for deployment {deployment}...")
    for chunk in stream_chat_completion(deployment, prompt):
        # Each chunk contains a response object with 'choices' etc.
        print(chunk.choices[0].delta.content or '', end='')  # Preserve streaming output
