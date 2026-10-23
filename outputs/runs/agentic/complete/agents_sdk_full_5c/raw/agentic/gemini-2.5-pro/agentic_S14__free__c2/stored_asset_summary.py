from openai import OpenAI
from storage_models import SummaryResult

def summarize_asset_text(text_content: str, max_length: int = 150) -> SummaryResult:
    """
    Summarizes text content using an OpenAI model.

    :param text_content: The text to be summarized.
    :param max_length: The desired maximum length of the summary in tokens.
    :return: A SummaryResult object.
    """
    # Assumes OPENAI_API_KEY environment variable is set
    client = OpenAI()
    model_name = "gpt-4o"

    system_prompt = f"Summarize the following text concisely. The summary should be approximately {max_length} tokens long."

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text_content},
        ],
        max_tokens=max_length,
        temperature=0.3,
    )
    
    summary_text = response.choices[0].message.content if response.choices else ""

    return SummaryResult(
        original_text=text_content,
        summary=summary_text.strip(),
        model_used=model_name,
    )
