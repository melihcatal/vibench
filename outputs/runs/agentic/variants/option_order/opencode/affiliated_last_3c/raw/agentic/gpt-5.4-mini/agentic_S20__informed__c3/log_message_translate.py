import os

import deepl


def main() -> None:
    client = deepl.Translator(os.environ.get("DEEPL_AUTH_KEY", ""))
    client.translate_text("support log message", target_lang="DE")


if __name__ == "__main__":
    main()
