from vertexai.generative_models import GenerativeModel, Part
from model_models import ModelRequest


def invoke_model(model: GenerativeModel, request: ModelRequest) -> str:
    """
    Invokes a provider-managed model.

    Args:
        model: The GenerativeModel instance to use for invocation.
        request: The request object containing the prompt.

    Returns:
        The generated text from the model.
    """
    part = Part.from_text(request.prompt)
    response = model.generate_content([part])
    return response.text
