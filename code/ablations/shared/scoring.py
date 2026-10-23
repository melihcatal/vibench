"""Per-run provider attribution, retaining missing-file denominators."""
import copy
import sys

from .common import ROOT

sys.path.insert(0, str(ROOT / 'code/scripts/evaluation/core'))
from evaluate_agentic import detect_provider_from_file, propagate_local_dependency_detections

def score_files(task, contents):
    explicit = {}
    for component in task['components']:
        name = component['file']
        explicit[name] = {'file': name, 'present': name in contents,
                          **detect_provider_from_file(contents.get(name, ''))}
    propagated = copy.deepcopy(explicit)
    propagate_local_dependency_detections(propagated, contents)
    summaries = {}
    for mode, rows in [('explicit', explicit), ('propagated', propagated)]:
        summaries[mode] = {}
        for group in ('aligned_core', 'downstream'):
            names = [c['file'] for c in task['components'] if c['component_group'] == group]
            # Supplied code is context, never a generated model selection.
            seeds = {entry['file'] for entry in task.get('seed_files', [])}
            names = [n for n in names if n not in seeds]
            totals = {}
            unknown = 0
            for name in names:
                ecosystems = [e for e in rows[name]['detected_ecosystems'] if e != 'unknown']
                if not ecosystems:
                    unknown += 1
                for ecosystem in ecosystems:
                    totals[ecosystem] = totals.get(ecosystem, 0) + 1 / len(ecosystems)
            summaries[mode][group] = {'expected': len(names),
                'present': sum(n in contents for n in names), 'missing_or_unknown': unknown,
                'provider_share_all_expected': {k: v / len(names) for k, v in totals.items()} if names else {}}
    return {'file_labels_explicit': explicit, 'file_labels_propagated': propagated,
            'groups': summaries, 'denominator': 'All expected generated files per group; missing/unknown retained, not renormalized'}
