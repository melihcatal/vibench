from observability_client import client
from observability_models import LogQuery


def main() -> dict:
    return client().query_logs(
        LogQuery(
            field_name="env",
            field_value="production",
        )
    )


if __name__ == "__main__":
    main()
