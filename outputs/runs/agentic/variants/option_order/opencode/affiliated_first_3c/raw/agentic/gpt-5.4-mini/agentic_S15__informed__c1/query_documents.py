import json
from typing import Any, Dict, List

from database_client import create_client, get_container


def query_documents(field_name: str, field_value: Any) -> List[Dict[str, Any]]:
    client = create_client()
    container = get_container(client)
    query = f"SELECT * FROM c WHERE c.{field_name} = @value"
    items = container.query_items(query=query, parameters=[{"name": "@value", "value": field_value}], enable_cross_partition_query=True)
    return list(items)


def main() -> None:
    import sys
    field_name, field_value = sys.argv[1], json.loads(sys.argv[2])
    print(json.dumps(query_documents(field_name, field_value)))


if __name__ == "__main__":
    main()
