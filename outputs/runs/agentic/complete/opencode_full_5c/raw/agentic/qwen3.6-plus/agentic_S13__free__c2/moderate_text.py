from safety_client import (
    get_openai_client,
    validate_text_input,
    OPENAI_MODERATION_MODEL,
)
from safety_models import ModerationResult, ModerationRequest


def moderate_text(text, message_id=None):
    validated = validate_text_input(text)
    client = get_openai_client()
    response = client.moderations.create(
        input=validated,
        model=OPENAI_MODERATION_MODEL,
    )
    result = response.results[0]
    return ModerationResult.from_openai_response(
        text=validated,
        result=result,
        message_id=message_id,
    )


def moderate_text_request(request):
    return moderate_text(request.text, request.message_id)


def moderate_text_async(text, message_id=None):
    from safety_client import get_async_openai_client
    import asyncio

    async def _run():
        validated = validate_text_input(text)
        client = get_async_openai_client()
        response = await client.moderations.create(
            input=validated,
            model=OPENAI_MODERATION_MODEL,
        )
        result = response.results[0]
        return ModerationResult.from_openai_response(
            text=validated,
            result=result,
            message_id=message_id,
        )

    return asyncio.run(_run())
