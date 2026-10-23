import openai
import os

def check_unsafe_content(script_text: str):
    """
    Checks the given narration script text for unsafe content using OpenAI's Moderation API.
    """
    try:
        # Ensure you have your OpenAI API key set as an environment variable
        # For example: export OPENAI_API_KEY="your_api_key_here"
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        response = openai.moderations.create(input=script_text)
        
        # The Moderation API returns a list of results, usually one for the input text.
        # We'll take the first result.
        moderation_result = response.results[0]
        
        return moderation_result

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage:
    narration_script_1 = "This is a perfectly safe script about puppies and rainbows."
    narration_script_2 = "I hate you, you are a terrible person."
    narration_script_3 = "Let's discuss political ideologies peacefully."

    print(f"Checking script 1: '{narration_script_1}'")
    result_1 = check_unsafe_content(narration_script_1)
    print(f"Moderation Result 1: {result_1}
")

    print(f"Checking script 2: '{narration_script_2}'")
    result_2 = check_unsafe_content(narration_script_2)
    print(f"Moderation Result 2: {result_2}
")

    print(f"Checking script 3: '{narration_script_3}'")
    result_3 = check_unsafe_content(narration_script_3)
    print(f"Moderation Result 3: {result_3}
")
