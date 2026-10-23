import json
import os

# Example: Use Mistral Chat API for summarization
# Configure with environment variable MISTRAL_API_KEY
import mistralai

client = mistralai.ChatClient(api_key=os.getenv("MISTRAL_API_KEY"))


def summarize_invoice(expense_json: str) -> str:
    """Generate a concise summary of the extracted expense fields."""
    # Convert to dict for easier JSON serialization in the prompt
    data = json.loads(expense_json)
    prompt = f"Summarize the following invoice in two sentences maximum:\n{json.dumps(data, ensure_ascii=False, indent=2)}"
    response = client.chat_completion(
        model="mistral-large-latest", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()  # First (and only) answer
