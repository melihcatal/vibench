import openai
import os

def summarize_text(text: str) -> str:
    """
    Calls a hosted LLM (OpenAI GPT-3.5-turbo) to summarize long text.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Please summarize the following text: {text}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

if __name__ == "__main__":
    example_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines,
    as opposed to the natural intelligence displayed by animals including humans.
    Leading AI textbooks define the field as the study of "intelligent agents":
    any device that perceives its environment and takes actions that maximize
    its chance of successfully achieving its goals. Colloquially, the term "artificial
    intelligence" is often used to describe machines that mimic "cognitive" functions
    that humans associate with the human mind, such as "learning" and "problem-solving".
    """
    summary = summarize_text(example_text)
    print("Original Text:")
    print(example_text)
    print("
Summary:")
    print(summary)
