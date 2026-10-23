import os
from openai import OpenAI

def summarize_records(records: list[dict], field_to_summarize: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    texts_to_summarize = [str(record.get(field_to_summarize, '')) for record in records if field_to_summarize in record]
    
    if not texts_to_summarize:
        return "No content available to summarize."

    combined_text = "\n---\n".join(texts_to_summarize)

    prompt = (
        "Summarize the following document records. Focus on the main themes and key information. "
        "Keep the summary concise and informative:\n\n" + combined_text
    )

    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return chat_completion.choices[0].message.content
