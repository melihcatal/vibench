from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summarize_message_processing_results(results_text: str) -> str:
    """
    Uses OpenAI GPT to summarize message processing results.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes lists of message processing results concisely."
            },
            {
                "role": "user",
                "content": f"Summarize the following processing results:\n{results_text}"
            }
        ],
        max_tokens=150,
        temperature=0.3
    )
    return response.choices[0].message.content
