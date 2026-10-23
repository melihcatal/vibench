import os
import google.generativeai as genai

def summarize_message(message_content: str) -> str:
    """Summarizes the content of a message using the Gemini API."""
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # Use a specific model that supports text generation and summarization
    model = genai.GenerativeModel("gemini-pro") # Concrete model identifier

    prompt = f"Summarize the following message content concisely: {message_content}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing message: {e}"

if __name__ == '__main__':
    sample_message = (
        "User U123 just placed an order for product P456. "
        "The order total was $99.99 and it included two items: "
        "Item A (SKU: A-001) and Item B (SKU: B-002). "
        "Shipping address: 123 Main St, Anytown, USA. "
        "Payment was successful via credit card ending in 4242." 
    )
    summary = summarize_message(sample_message)
    print(f"Original message:\n{sample_message}\n")
    print(f"Summary:\n{summary}")
