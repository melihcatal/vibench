import os
import google.generativeai as genai
from vision_models import TextSafetyResult

def check_text_for_safety(text_content: str) -> TextSafetyResult:
    """Checks text content for unsafe content using a generative AI model."""
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Analyze the following text for any unsafe, harmful, or policy-violating content. 
    Classify it as 'SAFE' or 'UNSAFE' and provide a brief reason if unsafe. 
    Text: """{text_content}""""""

    response = model.generate_content(prompt)
    return TextSafetyResult(original_text=text_content, safety_check_result=response.text)

if __name__ == '__main__':
    # Example usage for demonstration
    # Make sure GEMINI_API_KEY is set in your environment
    safe_text = "This is a picture of a cat playing with a toy."
    unsafe_text = "Harmful content goes here."

    print(f"Checking text for safety: \"{safe_text}\" ")
    try:
        safety_result_safe = check_text_for_safety(safe_text)
        print(f"Safety Check Result (Safe): {safety_result_safe.safety_check_result}")
    except Exception as e:
        print(f"Error checking safe text: {e}")

    print(f"\nChecking text for safety: \"{unsafe_text}\" ")
    try:
        safety_result_unsafe = check_text_for_safety(unsafe_text)
        print(f"Safety Check Result (Unsafe): {safety_result_unsafe.safety_check_result}")
    except Exception as e:
        print(f"Error checking unsafe text: {e}")
        print("Please ensure GEMINI_API_KEY is set.")
