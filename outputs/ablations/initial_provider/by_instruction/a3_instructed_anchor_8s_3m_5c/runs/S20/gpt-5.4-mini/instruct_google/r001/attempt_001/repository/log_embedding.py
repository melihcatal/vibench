from google.cloud import aiplatform


def main() -> None:
    aiplatform.init(project='google-cloud-project', location='us-central1')


if __name__ == '__main__':
    main()
