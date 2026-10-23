import os

from google.cloud import language_v1


def main() -> None:
    _ = os.getenv('GOOGLE_CLOUD_PROJECT')
    language_v1.LanguageServiceClient()


if __name__ == '__main__':
    main()
