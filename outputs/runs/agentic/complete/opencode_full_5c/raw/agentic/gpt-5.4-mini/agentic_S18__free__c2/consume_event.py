import os

from messaging_client import consume_one


def main() -> None:
    subscription = os.getenv("PUBSUB_SUBSCRIPTION", "events-sub")
    message = consume_one(subscription)
    print(message.payload if message else {})


if __name__ == "__main__":
    main()
