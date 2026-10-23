from observability_client import query_recent_by_field


def main() -> None:
    for event in query_recent_by_field("service", "api", minutes=30):
        print(event)


if __name__ == "__main__":
    main()
