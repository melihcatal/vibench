import google.generativeai as genai
import os

def visual_safety_text(payload, config=None):
    config = config or {}
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    text_to_check = payload["text"]

    # Using Generative AI to check for unsafe content
    # The API will automatically apply safety filters based on its configuration
    # We can prompt it to evaluate the safety of the text.
    prompt = f"Evaluate the following text for any unsafe content (e.g., hate speech, harassment, sexually explicit, dangerous content). Respond with 'SAFE' or 'UNSAFE' and a brief reason if unsafe.\n\nText: \"""\n{text_to_check}\n\""""

    response = model.generate_content(prompt)

    # The response.text will contain the model's assessment.
    # We might need to parse this depending on the desired output format.
    # For simplicity, we'll return the model's raw text response for safety assessment.
    safety_assessment = response.text.strip()

    return {"safety_assessment": safety_assessment}
