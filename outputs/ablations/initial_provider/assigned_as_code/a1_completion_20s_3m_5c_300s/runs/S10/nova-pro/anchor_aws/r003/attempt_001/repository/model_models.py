from.model_client import prepare_payload, parse_response


def summarize_text_model(payload, config=None):
    client = get_bedrock_client(config.get("region"))
    prompt = "Summarize the following text concisely:

" + payload["text"]
    payload = prepare_payload(prompt)
    response = client.converse(**payload)
    return parse_response(response)


def extract_json_model(payload, config=None):
    client = get_bedrock_client(config.get("region"))
    prompt = "Extract the following information in JSON format:

" + payload["text"]
    payload = prepare_payload(prompt)
    response = client.converse(**payload)
    return parse_response(response)


def answer_with_context_model(question, context, config=None):
    client = get_bedrock_client(config.get("region"))
    prompt = f"Answer the following question using the provided context:

Question: {question}
Context: {context}"
    payload = prepare_payload(prompt)
    response = client.converse(**payload)
    return parse_response(response)