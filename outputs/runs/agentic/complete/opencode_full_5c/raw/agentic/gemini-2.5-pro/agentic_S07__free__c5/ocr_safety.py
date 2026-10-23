import cohere
from document_client import get_cohere_client
from document_models import SafetyResult


def check_text_safety(text: str) -> SafetyResult:
    cohere_client = get_cohere_client()

    # Using a pre-trained model for simplicity.
    # For a real application, a fine-tuned model would be better.
    # The 'classify' endpoint with a public model is not a direct safety classifier,
    # so we use a generic model and interpret the results.
    # A better approach would be to use a dedicated content safety API.
    # For the purpose of this example, we use the command-nightly model
    # to check if the text is 'toxic' or 'benign'.

    try:
        response = cohere_client.classify(
            model="embed-english-v2.0",
            inputs=[text],
            examples=[
                cohere.ClassifyExample(text="you are a moron", label="toxic"),
                cohere.ClassifyExample(text="i hate you", label="toxic"),
                cohere.ClassifyExample(
                    text="this is a perfectly normal sentence", label="benign"
                ),
                cohere.ClassifyExample(text="I love documentation", label="benign"),
            ],
        )

        classification = response.classifications[0]
        is_safe = classification.prediction == "benign"
        confidence = classification.confidence

        return SafetyResult(is_safe=is_safe, confidence=confidence)
    except cohere.CohereError as e:
        # Handle API errors gracefully
        return SafetyResult(is_safe=True, confidence=0.0)
