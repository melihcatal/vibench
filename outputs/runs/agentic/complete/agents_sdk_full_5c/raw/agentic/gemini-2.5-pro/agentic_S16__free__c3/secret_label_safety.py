import openai
from security_client import get_openai_api_key
from security_models import TextSafetyResult

def check_text_safety(text: str) -> TextSafetyResult:
    """
    Checks secret labels or notes for unsafe text using OpenAI's Moderation API.

    Args:
        text: The input string to analyze.

    Returns:
        A TextSafetyResult object with the analysis outcome.
    """
    api_key = get_openai_api_key()
    if not api_key:
        raise ValueError("OpenAI API key is not configured.")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.moderations.create(
            input=text,
            model="text-moderation-latest"
        )
        
        moderation_result = response.results[0]
        flagged_categories = [
            category for category, flagged in moderation_result.categories if flagged
        ]

        return TextSafetyResult(
            text=text,
            is_safe=not moderation_result.flagged,
            flags=flagged_categories
        )
    except openai.APIError as e:
        print(f"OpenAI API error: {e}")
        # Return a default "unsafe" result in case of API failure for safety
        return TextSafetyResult(
            text=text,
            is_safe=False,
            flags=["api_error"]
        )

# Example usage would be in a different file.
# if __name__ == '__main__':
#     unsafe_label = "This label contains violent content just to trigger the filter."
#     safe_label = "production-database-credentials"

#     safety_check_unsafe = check_text_safety(unsafe_label)
#     print(f"Checking unsafe text: '{safety_check_unsafe.text}'")
#     print(f"Is safe? {safety_check_unsafe.is_safe}")
#     print(f"Flags: {safety_check_unsafe.flags}")

#     print("-" * 20)

#     safety_check_safe = check_text_safety(safe_label)
#     print(f"Checking safe text: '{safety_check_safe.text}'")
#     print(f"Is safe? {safety_check_safe.is_safe}")
#     print(f"Flags: {safety_check_safe.flags}")
