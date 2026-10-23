import google.generativeai as genai
import os

def check_annotation_safety(text_annotation: str):
    # Configure the generative AI model
    # Ensure GOOGLE_API_KEY environment variable is set or passed securely
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    # Use a prompt to guide the model for safety checking
    # Gemini Pro also has built-in safety filters, but a prompt can add specific context.
    prompt = f"""
    Analyze the following text for any unsafe content, including but not limited to hate speech,
    sexual content, violence, or self-harm. Indicate if it's safe or describe any identified issues.

    Text: "{text_annotation}"

    Response format: "SAFE" or "UNSAFE: [reason]"
    """

    response = model.generate_content(prompt)

    if response and response.candidates and response.candidates[0].content.parts:
        return response.candidates[0].content.parts[0].text
    return "Could not perform safety check."
