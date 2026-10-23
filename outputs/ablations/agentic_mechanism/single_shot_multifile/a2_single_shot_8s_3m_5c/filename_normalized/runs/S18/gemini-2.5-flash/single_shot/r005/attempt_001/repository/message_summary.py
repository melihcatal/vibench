import os
import openai

def summarize_message_payload(text_content: str) -> str:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes message payloads concisely."},
                {"role": "user", "content": f"Summarize the following message content:\n\n{text_content}"}
            ],
            max_tokens=100
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except openai.APIError as e:
        raise RuntimeError(f"OpenAI API error during summarization: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to summarize message payload: {e}")
