from openai import OpenAI
import os

def image_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('openai_api_key', os.environ.get('OPENAI_API_KEY')))

    # Combine all visual analysis results into a single string for summarization
    analysis_results = []
    if 'labels' in payload and payload['labels']:
        analysis_results.append(f"Detected labels: {', '.join([label['name'] for label in payload['labels']])}.")
    if 'description' in payload and payload['description']:
        analysis_results.append(f"Image description: {payload['description']}")
    if 'detected_text' in payload and payload['detected_text']:
        text_content = " ".join([text['text'] for text in payload['detected_text']])
        analysis_results.append(f"Detected text: \"{text_content}\".")
    if 'safe_search_results' in payload and payload['safe_search_results']:
        safety_info = ", ".join([f'{k}: {v}' for k, v in payload['safe_search_results'].items()])
        analysis_results.append(f"Safety analysis: {safety_info}.")
    if 'safety_scores' in payload and payload['safety_scores']:
        clarifai_safety_info = ", ".join([f'{k}: {v:.2f}' for k, v in payload['safety_scores'].items()])
        analysis_results.append(f"Clarifai safety scores: {clarifai_safety_info}.")

    full_analysis_text = " ".join(analysis_results).strip()

    if not full_analysis_text:
        return {'summary': "No visual analysis results provided to summarize."}

    prompt = f"Summarize the following visual analysis results concisely: {full_analysis_text}"

    response = client.chat.completions.create(
        model=config.get('openai_model', "gpt-4"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes image analysis results."},
            {"role": "user", "content": prompt}
        ]
    )

    summary = response.choices[0].message.content.strip()
    return {'summary': summary}
