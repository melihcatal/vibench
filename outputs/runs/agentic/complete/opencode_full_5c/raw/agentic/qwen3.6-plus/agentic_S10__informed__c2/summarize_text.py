from model_client import execute_llm_request, select_model_for_task
from model_models import LLMRequest, LLMResponse, build_system_prompt, truncate_text


def summarize_text(
    text: str,
    max_summary_length: int = 300,
    model: str = "gpt-4o",
    temperature: float = 0.3,
) -> LLMResponse:
    truncated = truncate_text(text, max_chars=100000)
    system = build_system_prompt(
        task_description="You are an expert summarizer. Provide a concise, accurate summary of the given text.",
        output_format=f"A clear summary of at most {max_summary_length} words.",
        constraints=[
            "Preserve key facts and main arguments",
            "Do not add information not present in the source",
            "Maintain a neutral, objective tone",
        ],
    )
    request = LLMRequest(
        model=model or select_model_for_task("summarization"),
        system_prompt=system,
        user_prompt=f"Summarize the following text:\n\n{truncated}",
        temperature=temperature,
        max_tokens=max_summary_length * 2,
    )
    return execute_llm_request(request)


def summarize_text_batch(
    texts: list[str],
    max_summary_length: int = 300,
    model: str = "gpt-4o",
    temperature: float = 0.3,
) -> list[LLMResponse]:
    results = []
    for text in texts:
        result = summarize_text(
            text,
            max_summary_length=max_summary_length,
            model=model,
            temperature=temperature,
        )
        results.append(result)
    return results
