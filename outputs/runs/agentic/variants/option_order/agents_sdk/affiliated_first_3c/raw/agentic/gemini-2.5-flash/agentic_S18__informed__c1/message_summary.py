import os
import google.generativeai as genai

def summarize_message_content(message_payload: str) -> str:
    """
    Summarizes the given message payload text using the Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following message content concisely:

{message_payload}"

    try:
        response = model.generate_content(prompt)
        if response.parts:
            # Join parts to form a complete response, handling potential multiple parts
            summary = "".join([part.text for part in response.parts])
            return summary.strip()
        elif response.text:
            return response.text.strip()
        else:
            return "Could not generate summary."
    except Exception as e:
        return f"Error summarizing content: {e}"

if __name__ == "__main__":
    sample_message = """
    This is a long message content that needs to be summarized.
    It contains details about a customer order, including item IDs, quantities,
    shipping address, and payment information. The order was placed on October 27, 2023,
    and is expected to ship by October 30, 2023. The total amount was $150.00.
    The customer is requesting a gift wrapping option for item 'SKU-789'.
    """
    
    # Ensure GOOGLE_API_KEY is set in your environment
    if os.environ.get("GOOGLE_API_KEY"):
        summary = summarize_message_content(sample_message)
        print("Original Message:")
        print(sample_message)
        print("\nSummary:")
        print(summary)
    else:
        print("Please set the GOOGLE_API_KEY environment variable to run this example.")
