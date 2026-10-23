import google.generativeai as genai
import os

def check_log_text_safety(log_message: str) -> dict:
    # Configure the Google Generative AI client
    # Ensure GOOGLE_API_KEY is set in your environment variables
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Use a model capable of content moderation
    # For safety, using a model like 'gemini-pro' with safety settings is a common approach.
    # Alternatively, more specialized moderation APIs might be available from Google Cloud.
    model = genai.GenerativeModel('gemini-pro')

    # Prompt the model to assess the safety of the log message
    prompt = (
        "Analyze the following log message for any unsafe content, "
        "such as personally identifiable information (PII), sensitive data, "
        "or inappropriate language. Respond with 'SAFE' if no unsafe content is found, "
        "otherwise, briefly describe the unsafe content found." \
        f"\n\nLog Message: \'{log_message}\'"
    )

    try:
        response = model.generate_content(prompt)
        # The response.text will contain the model's assessment.
        # For more structured safety analysis, you might integrate with specific safety APIs
        # or parse the model's output more rigorously.
        return {"assessment": response.text}
    except Exception as e:
        return {"error": f"Error checking log text safety: {e}"}

if __name__ == "__main__":
    # Example Usage:
    test_messages = [
        "User login successful for user_id: 12345, IP: 192.168.1.1",
        "An error occurred, details: Credit Card Number 1234-5678-9012-3456 failed validation.",
        "Application started normally.",
        "System health check passed."
    ]

    for msg in test_messages:
        safety_check_result = check_log_text_safety(msg)
        print(f"\nLog Message: \"{msg}\"\nSafety Assessment: {safety_check_result.get("assessment", safety_check_result.get("error"))}")
