import os
import google.generativeai as genai

def summarize_message_content(message_text: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    if not genai.get_default_model():
        # Fallback to a common model if default isn't set, e.g., 'gemini-pro'
        # In a production setting, you'd likely configure this explicitly.
        model = genai.GenerativeModel('gemini-pro')
    else:
        model = genai.get_default_model()

    prompt = f"Summarize the following message content concisely:

{message_text}"
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_API_KEY environment variable
    # from your terminal: export GOOGLE_API_KEY="your-gemini-api-key"

    example_message = "Customer order #12345 for items: Laptop (qty 1), Mouse (qty 1). Shipping address: 123 Main St, Anytown, USA. Payment status: completed. Order placed on 2023-10-26."
    summary = summarize_message_content(example_message)
    print("Original message:", example_message)
    print("Summary:", summary)
