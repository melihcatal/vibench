import os


def load_identity_config(config=None):
    config = dict(config or {})
    config.setdefault('tenant_id', os.environ.get('AZURE_TENANT_ID'))
    config.setdefault('client_id', os.environ.get('AZURE_CLIENT_ID'))
    config.setdefault('client_secret', os.environ.get('AZURE_CLIENT_SECRET'))
    config.setdefault('issuer', os.environ.get('AZURE_B2C_ISSUER'))
    config.setdefault('graph_base_url', 'https://graph.microsoft.com/v1.0')
    config.setdefault('translation_endpoint', os.environ.get('AZURE_TRANSLATOR_ENDPOINT', 'https://api.cognitive.microsofttranslator.com'))
    config.setdefault('translation_key', os.environ.get('AZURE_TRANSLATOR_KEY'))
    config.setdefault('translation_region', os.environ.get('AZURE_TRANSLATOR_REGION'))
    config.setdefault('moderation_endpoint', os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT'))
    config.setdefault('moderation_key', os.environ.get('AZURE_CONTENT_SAFETY_KEY'))
    config.setdefault('support_project', os.environ.get('OPENAI_PROJECT'))
    return config


def require_config(config, *keys):
    missing = [key for key in keys if not config.get(key)]
    if missing:
        raise RuntimeError('Missing configuration: ' + ', '.join(missing))
    return config
