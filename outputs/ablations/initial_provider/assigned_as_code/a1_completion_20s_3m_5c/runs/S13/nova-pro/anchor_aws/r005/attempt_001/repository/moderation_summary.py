from safety_client import get_comprehend_client
from safety_models import parse_response


def moderation_summary(payloads, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    responses = client.batch_detect_toxic_content(TextSegments=payloads, LanguageCode="en")
    summaries = [parse_response(response) for response in responses['ResultList']]
    return summaries