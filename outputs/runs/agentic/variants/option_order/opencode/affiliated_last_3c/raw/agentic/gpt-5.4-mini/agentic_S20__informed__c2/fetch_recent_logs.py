from observability_client import recent_logs


def main() -> list[dict]:
    return recent_logs({"service": "checkout-api", "status": "accepted"}, minutes=30)


if __name__ == "__main__":
    main()
