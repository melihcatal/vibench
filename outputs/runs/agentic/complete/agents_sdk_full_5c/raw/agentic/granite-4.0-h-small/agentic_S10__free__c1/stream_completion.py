import openai
import model_client

def stream_completion(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Streams token-by-token completion from a hosted LLM.
    Args:
        prompt (str): The initial prompt to continue.
        model (str): LLM model identifier (default: gpt-4o-mini).
    Yields:
        str: Each partial generated token (or chunk) as it is produced.
    """
    # Safety check on the prompt
    safe_prompt = model_client.check_prompt(prompt)
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": safe_prompt}],
        stream=True,
    )
    for chunk in response:
        # Each chunk contains .choices[0].text which holds the generated tokens so far
        partial = chunk.choices[0].text
        yield partial
