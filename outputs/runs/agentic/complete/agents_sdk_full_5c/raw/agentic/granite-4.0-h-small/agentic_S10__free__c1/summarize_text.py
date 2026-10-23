import openai
import model_client

def summarize_text(text: str, model: str = "gpt-4o-mini") -> str:
    """Summarizes the given text using the hosted OpenAI GPT-4o-mini model.
    Args:
        text (str): The text to summarize.
        model (str): The model identifier (default: gpt-4o-mini).
    Returns:
        str: The generated summary.
    """
    # Ensure the prompt complies with safety guidelines
    safe_prompt = model_client.check_prompt(text)
    # Call the model
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": f"Summarize the following text in under 150 words:\n        {safe_prompt}"}],
    )
    return response.choices[0].message.content
