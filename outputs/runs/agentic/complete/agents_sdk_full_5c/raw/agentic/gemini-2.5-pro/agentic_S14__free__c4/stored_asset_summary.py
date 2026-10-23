import os
import cohere
from storage_models import SummaryResult

def summarize_text(text: str) -> SummaryResult:
    """
    Summarizes a block of text using the Cohere API.

    Requires the COHERE_API_KEY environment variable.

    :param text: The text content to summarize.
    :return: A SummaryResult object.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.summarize(
            text=text,
            model="command",
            length="medium",
            extractiveness="auto"
        )
        
        summary = SummaryResult(
            id=response.id,
            summary=response.summary,
            original_text_length=len(text),
            summary_text_length=len(response.summary)
        )
        return summary
    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        raise
