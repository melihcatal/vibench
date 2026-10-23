"""
summarize_text.py - Calls a hosted OpenAI LLM to summarize long text.

Uses the OpenAI Chat Completions API with the gpt-4o model family.
"""

from model_client import get_openai_client, select_model, build_chat_messages
from model_models import LLMRequest, LLMResponse, build_summary_request


def summarize_text(
    text: str,
    model_family: str = "gpt-4o",
    max_words: int = 150,
    temperature: float = 0.3,
) -> LLMResponse:
    """
    Summarize the provided long text using OpenAI's hosted LLM.

    Args:
        text: The long text to summarize.
        model_family: OpenAI model family to use (e.g. "gpt-4o", "gpt-4o-mini").
        max_words: Target maximum word count for the summary.
        temperature: Sampling temperature for generation.

    Returns:
        LLMResponse containing the summary text and metadata.
    """
    request = build_summary_request(text, model_family, max_words)
    request.temperature = temperature

    client = get_openai_client()
    model_id = select_model(request.model_family)

    system_prompt = (
        "You are an expert summarizer powered by OpenAI. "
        "Provide concise, accurate summaries that capture the main points."
    )
    messages = build_chat_messages(
        system_prompt=system_prompt,
        user_content=request.user_content,
        format_instructions=None,
    )

    params = request.to_openai_params(model=model_id, messages=messages)

    completion = client.chat.completions.create(**params)

    if completion.choices and completion.choices[0].message:
        content = completion.choices[0].message.content
    else:
        content = ""

    usage = completion.usage
    return LLMResponse(
        text=content if content else "",
        model_used=model_id,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
        finish_reason=completion.choices[0].finish_reason if completion.choices else "",
        raw_response=completion,
    )


if __name__ == "__main__":
    sample_text = (
        "The rapid advancement of artificial intelligence has transformed numerous industries. "
        "In healthcare, AI systems assist in diagnosing diseases, predicting patient outcomes, "
        "and personalizing treatment plans. Machine learning algorithms can analyze vast amounts "
        "of medical data, including electronic health records, medical imaging, and genomic "
        "information, to identify patterns that human practitioners might miss. Natural language "
        "processing models are being used to extract insights from clinical notes and research "
        "literature. Despite these advances, challenges remain including data privacy concerns, "
        "algorithmic bias, and the need for regulatory frameworks to ensure safe and ethical "
        "deployment of AI in sensitive healthcare settings."
    )
    result = summarize_text(sample_text, model_family="gpt-4o", max_words=80)
    print(f"Model: {result.model_used}")
    print(f"Summary: {result.text}")
    print(f"Tokens: {result.total_tokens}")
