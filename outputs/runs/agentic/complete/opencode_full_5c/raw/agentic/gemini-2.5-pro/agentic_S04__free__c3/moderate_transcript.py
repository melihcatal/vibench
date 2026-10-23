import os
import cohere
from speech_models import ModerationRequest, ModerationResponse

COHERE_API_KEY = os.getenv("COHERE_API_KEY")


def moderate_text(request: ModerationRequest) -> ModerationResponse:
    """
    Moderates text using the Cohere API.
    """
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(COHERE_API_KEY)

    response = co.moderate(texts=[request.text], model="moderate-english-v3.0")

    first_result = response[0]

    # Simplified mapping from cohere categories to our model
    categories = []
    if first_result.flagged:
        for category, flagged in first_result.category_scores.items():
            if flagged:
                categories.append(category)

    return ModerationResponse(flagged=first_result.flagged, categories=categories)


if __name__ == "__main__":
    if not COHERE_API_KEY:
        print("Please set the COHERE_API_KEY environment variable.")
    else:
        safe_text = ModerationRequest(text="This is a perfectly normal sentence.")
        flagged_text = ModerationRequest(text="This is an example of toxic content.")

        safe_response = moderate_text(safe_text)
        print(f"'{safe_text.text}': Flagged - {safe_response.flagged}")

        flagged_response = moderate_text(flagged_text)
        print(
            f"'{flagged_text.text}': Flagged - {flagged_response.flagged}, Categories: {flagged_response.categories}"
        )
