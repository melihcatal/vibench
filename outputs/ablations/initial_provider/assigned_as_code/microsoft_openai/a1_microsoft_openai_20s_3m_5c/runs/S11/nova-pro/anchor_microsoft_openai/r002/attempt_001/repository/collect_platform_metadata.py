from invoke_platform_model import invoke_platform_model


def collect_platform_metadata(response):
    metadata = {
        'usage': response.usage,
        'model': response.model,
        'id': response.id
    }
    return metadata