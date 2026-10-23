from model_client import get_model
from model_models import InvokeRequest, InvokeResponse


def invoke_model(request: InvokeRequest) -> InvokeResponse:
    model = get_model()
    response = model.generate_content(request.prompt)

    first_candidate = response.candidates[0]

    return InvokeResponse(
        text=first_candidate.content.parts[0].text,
        metadata={
            "finish_reason": first_candidate.finish_reason.name,
        },
    )
