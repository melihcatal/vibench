import os

import google.generativeai as genai

from messaging_models import MessageSummaryRequest, MessageSummaryResponse

def summarize_message(request: MessageSummaryRequest) -> MessageSummaryResponse:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    genai.configure(api_key=api_key)

    # Use a specific Gemini model for text generation
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following message content:

{request.text}"

    response = model.generate_content(prompt)
    summary = response.text

    return MessageSummaryResponse(summary=summary)

if __name__ == '__main__':
    # Example Usage (requires GOOGLE_API_KEY environment variable set)
    message_content = """
    Customer order #12345 has been placed successfully. 
    Items: Laptop (Qty: 1), Mouse (Qty: 2). 
    Shipping address: 123 Main St, Anytown, USA. 
    Payment processed via credit card. Estimated delivery: 3-5 business days.
    """
    
    request = MessageSummaryRequest(text=message_content)
    response = summarize_message(request)
    print(f"Message Summary: {response.summary}")
