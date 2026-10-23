from deep_translator import DeepLTranslator


def main(query: str, target_language: str) -> str:
    return DeepLTranslator(
        api_key=None, source="auto", target=target_language
    ).translate(query)
