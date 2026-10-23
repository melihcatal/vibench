from observability_client import client
from observability_models import LogQuery


def main() -> dict:
    return client().query_logs(
        LogQuery(
            severity="error",
            text="exception",
            field_name="service",
            field_value="checkout-api",
        )
    )


if __name__ == "__main__":
    main()
