
import os
from openai import OpenAI

def summarize_message(text_content: str) -> str:
    """
    Summarizes the given text content using the OpenAI Chat Completions API.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI()

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text concisely."
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following text in one sentence: '{text_content}'"
                }
            ],
            max_tokens=100,
            temperature=0.5,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        print(f"An error occurred while calling OpenAI API: {e}")
        return "Error: Summary generation failed."

if __name__ == '__main__':
    # This is an example, not part of the required functionality.
    if os.getenv("OPENAI_API_KEY"):
        sample_text = "The new quantum computing chip, named 'Aurora', has successfully performed a complex simulation in minutes that would take traditional supercomputers years to complete. This breakthrough is expected to accelerate advancements in medicine, materials science, and artificial intelligence."
        summary = summarize_message(sample_text)
        print(f"Original: {sample_text}")
        print(f"Summary: {summary}")
