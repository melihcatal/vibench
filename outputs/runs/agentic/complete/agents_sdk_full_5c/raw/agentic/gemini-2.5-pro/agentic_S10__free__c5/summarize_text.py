from model_client import client
from model_models import SummaryResponse

def summarize_long_text(text_to_summarize: str) -> SummaryResponse:
    """
    Calls the Cohere API to summarize a long piece of text.
    """
    response = client.summarize(
        text=text_to_summarize,
        model='command',
        length='medium',
        extractiveness='low'
    )
    return SummaryResponse(summary=response.summary, id=response.id)
