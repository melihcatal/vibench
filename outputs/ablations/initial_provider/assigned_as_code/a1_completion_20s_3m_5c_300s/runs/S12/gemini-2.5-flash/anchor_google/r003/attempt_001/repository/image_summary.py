import google.generativeai as genai
import os


def image_summary(payload, config=None):
    config = config or {}
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel(config.get("model_name", "gemini-pro"))

    # Combine all available information into a prompt for the generative model
    prompt_parts = ["Summarize the following image analysis results:"]
    if "labels" in payload and payload["labels"]:
        prompt_parts.append(f"Labels: {', '.join([label['name'] for label in payload['labels']])}.")
    if "description" in payload and payload["description"]:
        prompt_parts.append(f"Description: {payload['description']}")
    if "detected_text" in payload and payload["detected_text"]:
        prompt_parts.append(f"Detected Text: \"""\n{payload['detected_text']}\n""".")
    if "safety_scores" in payload:
        safety_info = ', '.join([f"{k}: {v}" for k, v in payload['safety_scores'].items()])
        prompt_parts.append(f"Safety Scores: {safety_info}.")

    prompt = "\n".join(prompt_parts)

    response = model.generate_content(prompt)
    return {"summary": response.text}
