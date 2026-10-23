import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

def check_annotation_safety(annotation_text: str, config: dict = None) -> dict:
    config = config or {}
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = (
        "Analyze the following text for any unsafe content, including but not limited to "
        "hate speech, sexually explicit content, harassment, or dangerous content. "
        "Return 'safe' if no unsafe content is detected, otherwise return 'unsafe' "
        "and a brief reason.

"
        f"Text: {annotation_text}

Analysis:"
    )

    response = model.generate_content(
        prompt,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }
    )
    # The response.text might contain a summary or a direct answer based on the prompt.
    # We will assume the model directly answers "safe" or "unsafe: [reason]"
    # A more robust solution might parse the safety_ratings from response.candidates[0].safety_ratings
    # and interpret them. For this example, we rely on the prompt to guide the text output.
    
    result_text = response.text.lower().strip()
    if result_text == 'safe':
        return {'status': 'safe'}
    else:
        return {'status': 'unsafe', 'reason': result_text.replace('unsafe:', '').strip()}
