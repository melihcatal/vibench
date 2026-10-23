import openai
import os

def check_safety(text_to_check: str) -> dict:
    """
    Checks the given text for unsafe content using OpenAI's moderation API.
    
    Args:
        text_to_check: The text (secret label or note) to check.
        
    Returns:
        A dictionary containing the moderation result.
    """
    try:
        # It is recommended to load the OpenAI API key from environment variables
        # For example: openai.api_key = os.environ.get("OPENAI_API_KEY")
        # For demonstration, a placeholder is used.
        openai.api_key = os.getenv("OPENAI_API_KEY") 
        
        response = openai.moderations.create(input=text_to_check)
        return response.model_dump()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage:
    label = "This is a safe label."
    note = "This note contains some potentially offensive language like badword123."

    print(f"Checking label: '{label}'")
    label_safety_result = check_safety(label)
    print("Label safety result:", label_safety_result)

    print(f"\nChecking note: '{note}'")
    note_safety_result = check_safety(note)
    print("Note safety result:", note_safety_result)
