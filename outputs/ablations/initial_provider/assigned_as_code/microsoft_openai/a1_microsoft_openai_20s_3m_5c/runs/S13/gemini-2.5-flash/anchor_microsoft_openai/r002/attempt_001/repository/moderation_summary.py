import google.generativeai as genai

def moderation_summary(payload, config=None):
    config = config or {}
    genai.configure(api_key=config['api_key'])

    # Using a specific model, e.g., 'gemini-pro'
    model = genai.GenerativeModel(config.get('model_name', 'gemini-pro'))

    # The moderation_decisions payload is expected to be a list of dictionaries
    # E.g., [{'text': '...', 'toxicity': 0.8, 'decision': 'deny'}, ...]
    decisions_text = "\n".join([f"Text: {d.get('text', '')}, Decision: {d.get('decision', '')}, Reason: {d.get('reason', '')}" for d in payload['moderation_decisions']])

    prompt = f"Summarize the following moderation decisions:\n\n{decisions_text}\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        summary = response.text
    except Exception as e:
        summary = f"Error generating summary: {e}"

    return {'summary': summary}