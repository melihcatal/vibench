from.safety_models import create_moderation_request, parse_moderation_response

def moderation_summary(texts):
    summaries = []
    for text in texts:
        response = create_moderation_request(text)
        categories = parse_moderation_response(response)
        summaries.append(categories)
    return summaries