from google.cloud import language_v1
from translation_models import UnsafeContentCheckRequest, UnsafeContentCheckResponse
import os


def check_unsafe_copy(request: UnsafeContentCheckRequest) -> UnsafeContentCheckResponse:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=request.text,
        type=language_v1.Document.Type.PLAIN_TEXT,
        language=request.language,
    )

    # Perform content classification to detect potentially unsafe categories
    try:
        response = client.classify_text(request={"document": document})
        categories = response.categories

        unsafe_categories = [
            "/Adult",
            "/Sensitive Subjects",
            # Add more categories as deemed unsafe based on requirements
        ]

        is_safe = True
        details = ""
        detected_unsafe = []

        if categories:
            for category in categories:
                if (
                    category.name in unsafe_categories and category.confidence > 0.5
                ):  # Example confidence threshold
                    is_safe = False
                    detected_unsafe.append(
                        f"{category.name} (Confidence: {category.confidence:.2f})"
                    )

            if not is_safe:
                details = f"Potentially unsafe content detected in categories: {', '.join(detected_unsafe)}."
            else:
                details = "Content appears safe based on classification."
        else:
            details = "No specific categories detected. Content appears safe."

    except Exception as e:
        is_safe = False
        details = (
            f"Error during content classification: {str(e)}. Cannot confirm safety."
        )

    return UnsafeContentCheckResponse(is_safe=is_safe, details=details)


# Provider-identifying signal: google.cloud.language_v1 import
