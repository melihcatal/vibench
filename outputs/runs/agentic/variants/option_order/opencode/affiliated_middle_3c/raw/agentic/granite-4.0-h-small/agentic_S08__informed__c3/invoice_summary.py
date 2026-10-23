import json


# Hosted LLM inference via Mistral for summarization (later-step)
def summarize_invoice(extracted_json):
    # Convert dict to string payload for LLM
    prompt = f"You are a data summarizer. Summarize the following invoice details in 2-3 concise sentences:\n\n{json.dumps(extracted_json)}"
    # Call Mistral Chat (example SDK)
    response = mistral_chat_completion(prompt=prompt)
    return response["choices"][0]["message"]["content"]
