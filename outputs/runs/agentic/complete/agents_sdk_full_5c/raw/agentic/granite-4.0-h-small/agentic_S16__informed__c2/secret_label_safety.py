import argparse
from typing import Dict, List
from security_models import LabelMetadata, check_label_safety
from typing import Tuple


def analyze_labels(labels: LabelMetadata) -> Tuple[List[str], bool]:
    """
    Analyze secret labels for unsafe terms.
    Returns a tuple (offense_list, safe_bool).
    Safe_bool is True when no unsafe terms were found.
    """
    offenses = check_label_safety(labels)
    safe = len(offenses) == 0
    return offenses, safe


def main() -> None:
    parser = argparse.ArgumentParser(description='Scan secret labels for unsafe keywords.')
    # Generic placeholder for label payload; in practice you'd fetch from a provider
    parser.add_argument('--labels', type=str, required=True,
                        help='JSON-encoded dict of label key-value pairs')
    args = parser.parse_args()

    try:
        import json
        label_dict: Dict[str, Any] = json.loads(args.labels)
    except json.JSONDecodeError:
        raise ValueError('Invalid JSON supplied for --labels')

    offenses, safe = analyze_labels(label_dict)
    if safe:
        print('All labels are safe.')
    else:
        print(f'Found {len(offenses)} unsafe label(s):')
        for off in offenses:
            print(' -', off)

if __name__ == '__main__':
    main()
