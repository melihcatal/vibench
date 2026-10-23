from.model_client import get_text_analytics_client

def summarize_text(text):
    client = get_text_analytics_client()
    result = client.summarize(documents=[text])[0]
    return result.sentences

def extract_json(text):
    client = get_text_analytics_client()
    result = client.extract_key_phrases(documents=[text])[0]
    return result.key_phrases

def answer_with_context(question, context):
    client = get_text_analytics_client()
    result = client.answer_question(question=question, context=context)
    return result.answers[0].text

def stream_completion(prompt):
    client = get_text_analytics_client()
    result = client.complete(prompt=prompt)
    return result