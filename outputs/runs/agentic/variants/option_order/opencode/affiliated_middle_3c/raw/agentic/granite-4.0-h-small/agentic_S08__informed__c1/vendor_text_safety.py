import os
import dashscope
from dashscope import OpenAiClient


def moderate_vendor_notes(notes: str) -> dict:
    """Use DashScope Qwen model to assess the safety of vendor notes.

    Returns a dict with:
      - moderation: bool (True = safe)
      - flagged_categories: list of detected unsafe categories
      - raw_response: the full API response (for debugging)
    """
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("Set DASHSCOPE_API_KEY environment variable")
    client = OpenAiClient(api_key)
    # Define the prompt for the moderation task
    prompt = (
        "You are an AI content safety moderator. Assess the following vendor note for any harmful\ncontent. Return JSON with two keys: 'moderation' (boolean: True if safe), and\n'flagged_categories' (list of strings describing any unsafe categories, e.g. ['hate', 'sexual']).\nDo not include any explanations or other fields.\n---\nNote:\n{notes}"
    ).format(notes=notes)
    response = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    # Expect the model to reply with a JSON string in the assistant message content
    assistant_msg = response.choices[0].message.content.strip()
    try:
        moderation_result = json.loads(assistant_msg)
    except json.JSONDecodeError:
        return {
            "moderation": False,
            "flagged_categories": [],
            "raw_response": assistant_msg,
        }
    return moderation_result


# Example usage (run as a script)
if __name__ == "__main__":
    demo_note = "Vendor mentions paying bribes and includes a price quote of $5000."
    result = moderate_vendor_notes(demo_note)
    print(result)
    # Example with safe note
    safe_note = "Vendor is under contract and supplies widgets quarterly."
    print(moderate_vendor_notes(safe_note))
