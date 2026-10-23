import textwrap

from observability_client import get_safety_model

def metric_annotation_safety(payload, config=None):
    config = config or {}
    safety_model = get_safety_model()

    text_to_check = payload["annotation_text"]

    # Using Vertex AI's TextGenerationModel for content safety checks.
    # The actual safety check would involve evaluating the model's response
    # for attributes like toxicity, sentiment, etc., or using a dedicated safety API if available.
    # For this example, we'll ask the model to identify if the text is 'unsafe'.
    prompt = textwrap.dedent(f"""
    Analyze the following text and determine if it contains any unsafe or inappropriate content. 
    Respond with 'SAFE' if the content is clean, and 'UNSAFE' followed by a brief reason if it is not. 

    Text: """{text_to_check}"""

    Analysis:
    """)

    response = safety_model.predict(
        prompt,
        temperature=0.0,  # Aim for deterministic output for safety checks
        max_output_tokens=100
    )

    safety_report = response.text.strip()

    is_safe = "UNSAFE" not in safety_report.upper()

    return {"annotation_text": text_to_check, "is_safe": is_safe, "safety_report": safety_report}
