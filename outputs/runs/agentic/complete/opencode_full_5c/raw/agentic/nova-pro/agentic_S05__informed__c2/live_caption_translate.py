import deepl

DEEPL_AUTH_KEY = "your-deepl-auth-key"

client = deepl.Client(DEEPL_AUTH_KEY)


def live_caption_translate(caption):
    pass


if __name__ == "__main__":
    live_caption_translate("sample caption")
