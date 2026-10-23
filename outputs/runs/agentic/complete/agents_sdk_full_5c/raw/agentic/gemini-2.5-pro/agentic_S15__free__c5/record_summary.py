import os
import openai

def summarize_record(record_text: str) -> str:
    """
    Summarizes the text content of a record using an OpenAI model.

    This function requires the OPENAI_API_KEY environment variable to be set.

    Provider: OpenAI
    """
    # The OpenAI client uses the OPENAI_API_KEY environment variable by default.
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{record_text}"}
            ],
            temperature=0.5,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return "Error generating summary."
