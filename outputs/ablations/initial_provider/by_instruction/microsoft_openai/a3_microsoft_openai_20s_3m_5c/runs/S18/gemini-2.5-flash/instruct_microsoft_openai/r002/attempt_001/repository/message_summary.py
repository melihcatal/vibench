from openai import OpenAI
import os

def summarize_message(message_content: str) -> str:
    """
    Summarizes the content of a message using OpenAI's GPT models.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Concrete model identifier
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes message content."},
                {"role": "user", "content": f"Please summarize the following message content:

{message_content}"
                }
            ],
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"Error summarizing message with OpenAI: {e}")
        return "Summary generation failed."

if __name__ == "__main__":
    # Example usage
    sample_message_content = """
    {
        "id": "order-abc-123",
        "type": "OrderProcessed",
        "data": {
            "orderId": "ABC-123",
            "customerName": "Alice Smith",
            "items": [
                {"productId": "P001", "name": "Laptop", "quantity": 1, "price": 1200.00},
                {"productId": "P005", "name": "Mouse", "quantity": 1, "price": 25.00}
            ],
            "totalAmount": 1225.00,
            "currency": "USD",
            "status": "completed"
        },
        "timestamp": "2023-10-27T10:00:00Z"
    }
    """
    summary = summarize_message(sample_message_content)
    print(f"Message Summary: {summary}")
