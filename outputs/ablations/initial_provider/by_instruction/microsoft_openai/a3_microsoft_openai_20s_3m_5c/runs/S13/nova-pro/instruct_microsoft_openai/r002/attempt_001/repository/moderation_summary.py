from.safety_models import create_moderation_request, parse_moderation_response

def summarize_moderation(texts):
    summaries = []
    for text in texts:
        response = create_moderation_request(text)
        categories = parse_moderation_response(response)
        summaries.append({'text': text, 'categories': categories})
    return summaries