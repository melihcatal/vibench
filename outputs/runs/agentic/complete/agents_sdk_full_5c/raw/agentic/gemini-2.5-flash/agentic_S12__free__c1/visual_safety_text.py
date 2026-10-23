import os
import google.generativeai as genai
from typing import List

def check_text_for_safety(text_content: str):
    """Checks generated visual labels or descriptions for unsafe text using Google's Gemini Pro model."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    # The prompt explicitly asks the model to act as a content moderator
    prompt = f"Review the following text for safety and content policy violations. Categorize it as 'SAFE' or 'UNSAFE', and if unsafe, briefly explain why. Text: \"{text_content}\""

    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == '__main__':
    # Example usage
    safe_text = "A beautiful sunset over the mountains."
    print(f"Checking safe text: \"{safe_text}\"")
    safety_result_safe = check_text_for_safety(safe_text)
    print(f"Result: {safety_result_safe}\n")

    # Example of potentially unsafe text (adjust as needed for actual policy testing)
    # The model's safety classifications might vary, so direct output comparison might not be stable.
    # The goal here is to demonstrate the call, not to guarantee a specific safety verdict.
    unsafe_text = "I will hurt you." # Simplified for demonstration purposes
    print(f"Checking potentially unsafe text: \"{unsafe_text}\"")
    safety_result_unsafe = check_text_for_safety(unsafe_text)
    print(f"Result: {safety_result_unsafe}\n")
