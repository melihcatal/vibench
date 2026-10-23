from storage_client import get_comprehend_client
from storage_models import SummaryResult


def summarize_stored_asset_content(text: str, language_code: str = "en", config: dict = None) -> SummaryResult:
    config = config or {}
    comprehend_client = get_comprehend_client(region_name=config.get("region"))
    # For summarization, we can extract key phrases as a proxy
    response = comprehend_client.detect_key_phrases(
        Text=text,
        LanguageCode=language_code
    )
    key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]
    return SummaryResult(summary_text="; ".join(key_phrases))
