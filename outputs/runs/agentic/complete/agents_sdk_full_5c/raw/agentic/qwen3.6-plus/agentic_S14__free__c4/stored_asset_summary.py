"""Summarize content extracted from a stored asset using Amazon Bedrock."""

import json
from typing import Optional

from storage_client import S3ClientFactory
from storage_models import SummaryRequest, SummaryResult


DEFAULT_BEDROCK_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def summarize_stored_asset(
    text: str,
    model_id: str = DEFAULT_BEDROCK_MODEL_ID,
    max_tokens: int = 512,
    temperature: float = 0.3,
) -> SummaryResult:
    """
    Generate a summary of text extracted from a stored asset using Amazon Bedrock.

    Invokes the Amazon Bedrock Converse API (bedrock-runtime.us-east-1.amazonaws.com)
    with a foundational model (e.g., Anthropic Claude 3 Sonnet) to produce
    a concise summary of the provided text content.

    Args:
        text: The source text to summarize (typically OCR or extracted content).
        model_id: Bedrock model identifier. Defaults to
                  'anthropic.claude-3-sonnet-20240229-v1:0'.
        max_tokens: Maximum number of tokens in the generated summary.
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative).

    Returns:
        SummaryResult containing the generated summary and model metadata.

    Raises:
        botocore.exceptions.ClientError: If the model is unavailable or
            access to Amazon Bedrock is not configured.
    """
    factory = S3ClientFactory()
    bedrock_client = factory.get_bedrock_runtime_client()

    system_prompt = (
        "You are a document summarization assistant. "
        "Provide a concise, accurate summary of the provided text. "
        "Focus on key information, entities, and main points. "
        "Return only the summary without preamble."
    )

    user_message = {
        "role": "user",
        "content": [{"text": f"Summarize the following content:\n\n{text}"}],
    }

    converse_params = {
        "modelId": model_id,
        "messages": [user_message],
        "system": [{"text": system_prompt}],
        "inferenceConfig": {
            "maxTokens": max_tokens,
            "temperature": temperature,
        },
    }

    response = bedrock_client.converse(**converse_params)

    summary_text = ""
    output_content = response.get("output", {}).get("message", {}).get("content", [])
    for content_block in output_content:
        summary_text += content_block.get("text", "")

    usage = response.get("usage", {})

    return SummaryResult(
        summary=summary_text.strip(),
        model_id=model_id,
        token_usage={
            "input_tokens": usage.get("inputTokens", 0),
            "output_tokens": usage.get("outputTokens", 0),
            "total_tokens": usage.get("totalTokens", 0),
        },
    )


def summarize_with_claude_haiku(
    text: str,
    max_tokens: int = 512,
    temperature: float = 0.3,
) -> SummaryResult:
    """
    Summarize text using the lighter-weight Anthropic Claude 3 Haiku model
    on Amazon Bedrock for faster, cost-effective summaries.

    Uses model ID 'anthropic.claude-3-haiku-20240307-v1:0' on the
    bedrock-runtime endpoint.

    Args:
        text: Source text to summarize.
        max_tokens: Maximum output tokens.
        temperature: Sampling temperature.

    Returns:
        SummaryResult with the generated summary.
    """
    return summarize_stored_asset(
        text=text,
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        max_tokens=max_tokens,
        temperature=temperature,
    )


def summarize_with_llama(
    text: str,
    max_tokens: int = 512,
    temperature: float = 0.3,
) -> SummaryResult:
    """
    Summarize text using Meta Llama 3 on Amazon Bedrock.

    Uses model ID 'meta.llama3-70b-instruct-v1:0' via the
    bedrock-runtime.us-east-1.amazonaws.com endpoint.

    Args:
        text: Source text to summarize.
        max_tokens: Maximum output tokens.
        temperature: Sampling temperature.

    Returns:
        SummaryResult with the generated summary.
    """
    factory = S3ClientFactory()
    bedrock_client = factory.get_bedrock_runtime_client()

    prompt = (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        "You are a helpful summarization assistant. "
        "Provide a concise summary of the provided content.<|eot_id|>"
        "<|start_header_id|>user<|end_header_id|>\n\n"
        f"Summarize: {text}<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>\n\n"
    )

    native_params = {
        "prompt": prompt,
        "max_gen_len": max_tokens,
        "temperature": temperature,
    }

    response = bedrock_client.invoke_model(
        modelId="meta.llama3-70b-instruct-v1:0",
        body=json.dumps(native_params),
        contentType="application/json",
        accept="application/json",
    )

    response_body = json.loads(response.get("body").read())
    summary_text = response_body.get("generation", "").strip()

    return SummaryResult(
        summary=summary_text,
        model_id="meta.llama3-70b-instruct-v1:0",
        token_usage={
            "input_tokens": response_body.get("prompt_token_count", 0),
            "output_tokens": response_body.get("generation_token_count", 0),
            "total_tokens": response_body.get("prompt_token_count", 0)
            + response_body.get("generation_token_count", 0),
        },
    )
