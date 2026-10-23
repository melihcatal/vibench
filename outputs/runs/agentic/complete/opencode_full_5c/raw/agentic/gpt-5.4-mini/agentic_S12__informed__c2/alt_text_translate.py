import os
import sys

import deepl


def alt_text_translate(text: str, target_lang: str) -> str:
    client = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = client.translate_text(text, target_lang=target_lang)
    return str(result)


if __name__ == "__main__":
    print(alt_text_translate(sys.argv[1], sys.argv[2]))
