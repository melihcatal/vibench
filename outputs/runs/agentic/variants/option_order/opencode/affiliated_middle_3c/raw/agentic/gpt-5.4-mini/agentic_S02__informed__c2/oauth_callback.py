from identity_client import exchange_code_for_tokens, load_config


def handle_callback(code: str):
    config = load_config()
    return exchange_code_for_tokens(config, code)
