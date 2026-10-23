from model_client import build_platform_client, get_platform_deployment


def select_platform_resource(payload, config=None):
    client = build_platform_client(config)
    deployment = get_platform_deployment(config)
    return {'client': client, 'deployment': deployment, 'payload': payload}
