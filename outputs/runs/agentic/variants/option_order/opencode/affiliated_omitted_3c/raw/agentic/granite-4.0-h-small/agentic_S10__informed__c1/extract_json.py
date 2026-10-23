import dashscope


def extract_json(
    text: str,
    prompt: str = "Extract the relevant structured data from the following text as JSON:",
) -> dict:
    """Extract structured JSON from plain text using DashScope Qwen model.

    Args:
        text (str): The input text to parse.
        prompt (str, optional): Prompt to control extraction.

    Returns:
        dict: Parsed JSON dictionary.
    """
    client = dashscope.TextGeneration(api_key="${DASHSCOPE_API_KEY}")
    response = client.chat(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt + "\n\n" + text}],
        max_tokens=200,
    )
    return response.choices[0].message.parse_json()
