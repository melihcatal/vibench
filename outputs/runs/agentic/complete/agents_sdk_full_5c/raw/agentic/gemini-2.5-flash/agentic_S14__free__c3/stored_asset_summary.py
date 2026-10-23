import os
import boto3
import json
from storage_client import get_bedrock_runtime_client
from storage_models import AssetSummaryResult

def summarize_asset_content(text_content: str, max_tokens: int = 500) -> AssetSummaryResult or None:
    """
    Summarizes text content using an LLM on AWS Bedrock (e.g., Anthropic Claude).

    Args:
        text_content (str): The text to summarize.
        max_tokens (int): The maximum number of tokens for the summary.

    Returns:
        AssetSummaryResult or None: The summarized text, or None if an error occurs.
    """
    bedrock_runtime = get_bedrock_runtime_client()
    model_id = "anthropic.claude-v2" # Or "anthropic.claude-instant-v1"

    prompt = f"""Human: Summarize the following document concisely and accurately:\n\n<document>\n{text_content}\n</document>\n\nAssistant:"""

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": max_tokens,
        "temperature": 0.1,
        "top_p": 0.9,
    })

    try:
        print(f"Invoking Bedrock model '{model_id}' for summarization...")
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get('body').read())
        summary_text = response_body.get('completion')

        if summary_text:
            print("Summarization successful.")
            return AssetSummaryResult(summary_text=summary_text.strip())
        else:
            print("No summary text found in the model response.")
            return None

    except Exception as e:
        print(f"Error summarizing asset content with Bedrock: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    # This example assumes you have text already extracted, e.g., from an OCR step.
    # Ensure AWS credentials are configured and Bedrock access is granted to Claude v2.

    _long_sample_text = (
        "The Amazon rainforest is the largest tropical rainforest in the world, covering much of "
        "northwestern South America. It spans across nine countries, with the majority (60%) in Brazil. "
        "It is home to an incredible array of biodiversity, including millions of species of insects, "
        "tens of thousands of plants, and thousands of birds and mammals. The Amazon River, the second "
        "longest river in the world, flows through the heart of the forest. The rainforest plays a crucial "
        "role in regulating the Earth's climate by absorbing vast amounts of carbon dioxide. "
        "However, it is under constant threat from deforestation, primarily due to cattle ranching, "
        "agriculture, logging, and mining. Conservation efforts are underway to protect this vital ecosystem. "
        "Recent studies have highlighted the accelerating loss of forest cover, raising concerns about "
        "the long-term health of the planet."
    )

    print(f"\nOriginal Text (length: {len(_long_sample_text)} chars):\n---\n{_long_sample_text[:300]}...\n---")

    summary_result = summarize_asset_content(_long_sample_text, max_tokens=200)

    if summary_result:
        print(f"\nSummary:\n---\n{summary_result.summary_text}\n---")
    else:
        print("Failed to summarize content.")
