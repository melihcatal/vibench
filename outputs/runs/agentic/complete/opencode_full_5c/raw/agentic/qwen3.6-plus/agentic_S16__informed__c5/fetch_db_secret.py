import os
from security_models import SecretRequest, SecretResponse, SecretType
from security_client import fetch_secret_response


def fetch_db_secret(
    secret_id: str,
    version_id: str = None,
    version_stage: str = "AWSCURRENT",
    region: str = None,
) -> SecretResponse:
    request = SecretRequest(
        secret_id=secret_id,
        secret_type=SecretType.DATABASE,
        version_id=version_id,
        version_stage=version_stage,
        region=region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )
    response = fetch_secret_response(request)
    return response


def parse_db_connection_string(secret_response: SecretResponse) -> dict:
    value = secret_response.secret_value
    if value.startswith("postgresql://") or value.startswith("mysql://"):
        parts = {}
        if "://" in value:
            protocol, rest = value.split("://", 1)
            parts["protocol"] = protocol
            if "@" in rest:
                creds, host_port = rest.split("@", 1)
                if ":" in creds:
                    parts["username"], parts["password"] = creds.split(":", 1)
                if "/" in host_port:
                    host_db = host_port.split("/", 1)
                    host_part = host_db[0]
                    parts["database"] = host_db[1] if len(host_db) > 1 else ""
                    if ":" in host_part:
                        parts["host"], parts["port"] = host_part.split(":", 1)
                    else:
                        parts["host"] = host_part
                        parts["port"] = "5432" if protocol == "postgresql" else "3306"
                else:
                    parts["host"] = host_port
        return parts
    return {"connection_string": value}


if __name__ == "__main__":
    secret_id = os.environ.get("DB_SECRET_ID", "prod/database/postgres-primary")
    result = fetch_db_secret(secret_id)
    print(f"Retrieved DB secret for: {result.secret_id}")
    conn_info = parse_db_connection_string(result)
    print(f"Connection info keys: {list(conn_info.keys())}")
