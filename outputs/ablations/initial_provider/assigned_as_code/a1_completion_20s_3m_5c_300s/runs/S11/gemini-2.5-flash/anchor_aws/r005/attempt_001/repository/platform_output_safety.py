import google.generativeai as genai
import os

def check_platform_output_safety(text_output):
    # Configure the API key if not already configured globally
    # genai.configure(api_key="YOUR_API_KEY") # Assume API key is set via environment variable GOOGLE_API_KEY

    # This is a simplified example of using Google's safety settings
    # In a real application, you would typically integrate with a dedicated content moderation API
    # or use the safety features provided by the generative model itself.

    # For demonstration, we'll simulate a safety check using a known unsafe phrase
    unsafe_keywords = ["harmful", "dangerous", "unethical"]
    
    safety_flags = {
        "HARM_CATEGORY_HARASSMENT": False,
        "HARM_CATEGORY_HATE_SPEECH": False,
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": False,
        "HARM_CATEGORY_DANGEROUS_CONTENT": False,
    }

    for keyword in unsafe_keywords:
        if keyword in text_output.lower():
            safety_flags["HARM_CATEGORY_DANGEROUS_CONTENT"] = True # Simulate a flag
            break
    
    return {"text": text_output, "safety_flags": safety_flags, "is_safe": not any(safety_flags.values())}

