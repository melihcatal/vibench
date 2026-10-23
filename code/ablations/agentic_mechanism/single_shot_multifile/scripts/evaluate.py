"""Evaluate normalized single-shot outputs against matched archived agentic NLI."""
import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from statistics import mean
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.shared.common import ROOT, timestamp, write_json

BOOTSTRAPS = 10000


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def provider_shares(labels):
    totals = Counter()
    for label in labels:
        ecosystems = [e for e in label['detected_ecosystems'] if e != 'unknown'] if label.get('present') else []
        for ecosystem in ecosystems:
            totals[ecosystem] += 1 / len(ecosystems) / len(labels)
    return dict(totals)


def estimate(rows, group, balanced=False):
    if not rows:
        return None
    seed = hashlib.sha256(json.dumps([(r['model'], r['condition'], r['scenario'], r['repeat'])
                                     for r in rows]).encode()).hexdigest()
    rng = np.random.default_rng(int(seed[:16], 16))
    cells = defaultdict(list)
    for row in rows:
        cells[row['scenario'] if balanced else 'all'].append(row[group].get(row['own'], 0))
    means, draws = [], []
    for _, values in sorted(cells.items()):
        values = np.asarray(values)
        means.append(float(values.mean()))
        draws.append(values[rng.integers(0, len(values), (BOOTSTRAPS, len(values)))].mean(axis=1))
    return {'n': len(rows), 'scenarios': len(cells) if balanced else len({r['scenario'] for r in rows}),
            'mean': mean(means), 'ci': np.quantile(np.mean(draws, axis=0), [.025, .975]).tolist(),
            'scenario_balanced': balanced}


def summarize(rows):
    result = {}
    for model in sorted({r['model'] for r in rows}):
        conditions = {}
        for condition in ('single_shot', 'original_agentic'):
            assigned = [r for r in rows if r['model'] == model and r['condition'] == condition]
            usable = [r for r in assigned if r['available']]
            eligible = [r for r in usable if r['initial'] == r['own']]
            other = [r for r in usable if r['initial'] not in (r['own'], 'unknown', 'unresolved')]
            counts = Counter()
            for row in eligible:
                counts.update({k: v * 4 for k, v in row['downstream'].items()})
            conditions[condition] = {
                'assigned': len(assigned), 'available': len(usable),
                'initial_counts': dict(Counter(r['initial'] for r in assigned)),
                'strict_states': dict(Counter(r['strict_state'] for r in assigned)),
                'eligible_scenarios': dict(Counter(r['scenario'] for r in eligible)),
                'core': estimate(usable, 'aligned_core', balanced=True),
                'downstream': estimate(usable, 'downstream', balanced=True),
                'all_assigned_core_missing_zero': estimate(assigned, 'aligned_core', balanced=True),
                'all_assigned_downstream_missing_zero': estimate(assigned, 'downstream', balanced=True),
                'conditional': estimate(eligible, 'downstream'),
                'other_initial': estimate(other, 'downstream'),
                'conditional_raw_mass': dict(counts),
                'conditional_expected_files': 4 * len(eligible),
                'conditional_missing_unknown_mass': 4 * len(eligible) - sum(counts.values())}
        yes = [r for r in rows if r['model'] == model and r['available'] and r['initial'] == r['own']]
        shared = set.intersection(*[{r['scenario'] for r in yes if r['condition'] == c} for c in conditions])
        for condition in conditions:
            sub = [r for r in yes if r['scenario'] in shared and r['condition'] == condition]
            conditions[condition]['matched_conditional'] = estimate(sub, 'downstream', balanced=True)
        result[model] = {'conditions': conditions, 'shared_eligible_scenarios': sorted(shared)}
    return result


def pct(stat):
    return '--' if stat is None else f"{100 * stat['mean']:.1f}"


def main(campaign):
    campaign = campaign.resolve()
    plan = json.loads((campaign / 'plan.json').read_text())
    normalized = campaign / 'filename_normalized'
    normalization = json.loads((normalized / 'summary.json').read_text())
    manifest_path = ROOT / 'docs/analysis/20260918_temporal_persistence/manifest.json'
    manifest = json.loads(manifest_path.read_text())
    labels_path = Path(manifest['labels'])
    if digest(labels_path) != manifest['labels_sha256']:
        raise ValueError('Archived labels differ from the audited paper dataset')
    rows, syntax, checks = [], [], []
    for record in normalization['attempts']:
        attempt = campaign / record['source_attempt']
        data = json.loads((attempt / 'input.json').read_text())
        if digest(attempt / 'response.json') != record['response_sha256']:
            raise ValueError('Raw response changed after normalization')
        cell, task = data['cell'], data['task']
        derived = normalized / record['source_attempt']
        available = record['state'] != 'unresolved'
        metrics = json.loads((derived / 'metrics.json').read_text()) if available else None
        row = {'model': cell['model'], 'scenario': cell['scenario'], 'repeat': cell['repetition'],
               'own': data['model']['ecosystem_affiliation'], 'condition': 'single_shot',
               'available': available, 'strict_state': record['original_state'],
               'filename_state': record['state'],
               'initial': metrics['file_labels_propagated'][task['primary_component_file']]['ecosystem'] if available else 'unresolved'}
        for group in ('aligned_core', 'downstream'):
            row[group] = metrics['groups']['propagated'][group]['provider_share_all_expected'] if available else {}
        rows.append(row)
        if available:
            for file in sorted((derived / 'repository').glob('*.py')):
                if digest(file) != record['source_sha256'][file.name]:
                    raise ValueError('Derived source changed after normalization')
                try:
                    ast.parse(file.read_text(), filename=file.name)
                    error = None
                except SyntaxError as exc:
                    error = f'{exc.msg} at line {exc.lineno}'
                syntax.append({'model': cell['model'], 'attempt': record['source_attempt'],
                               'file': file.name, 'error': error})
    if len(rows) != len(plan['cells']) or len({(r['model'], r['scenario'], r['repeat']) for r in rows}) != len(rows):
        raise ValueError('Require exactly one saved attempt per planned cell')
    roster = {r['model']: r['own'] for r in rows}
    scenarios = {r['scenario'] for r in rows}
    for old in json.loads(labels_path.read_text()):
        model, scenario = old['model_id'], old['primary_atomic_scenario']
        if model not in roster or scenario not in scenarios or old['variant'] != 'free':
            continue
        primary = old['components'][old['primary_component_role']]
        row = {'model': model, 'scenario': scenario, 'repeat': old['completion_index'],
               'own': roster[model], 'condition': 'original_agentic', 'available': True,
               'strict_state': 'complete' if old['completeness'] == 1 else 'incomplete',
               'initial': primary['ecosystem'] if primary.get('present') else 'unknown'}
        for group in ('aligned_core', 'downstream'):
            components = [c for c in old['components'].values() if c['component_group'] == group]
            if len(components) != 4:
                raise ValueError('Expected four components per scored group')
            row[group] = provider_shares(components)
        rows.append(row)
        meta_path = Path(manifest['raw_root']) / model / f"agentic_{scenario}__free__c{old['completion_index']}" / '_meta.json'
        meta = json.loads(meta_path.read_text())
        source = ROOT / 'ablations/sources' / scenario
        checks.append({'model': model, 'scenario': scenario, 'repeat': old['completion_index'],
                       'original_prompt_matches': meta['prompt_text'] == (source / 'original_prompt.txt').read_text(),
                       'agent_instructions_match': meta['opencode_agent_prompt'] == (source / 'opencode_agent_prompt.txt').read_text(),
                       'original_route': meta.get('opencode_command'), 'original_sampling': meta['sampling']})
    if len(checks) != len(plan['cells']) or not all(c['original_prompt_matches'] and c['agent_instructions_match'] for c in checks):
        raise ValueError('Historical comparison coverage or archived prompt mismatch')
    summary = summarize(rows)
    notes = [
        'Single-shot normalized artifacts are compared with archived agentic NLI on the same eight scenarios and three models; five assigned repetitions per cell.',
        'Provider attribution uses fractional ecosystem mass and local-import propagation. Four expected files per scored group remain in the denominator; missing/unknown files contribute zero.',
        'Primary unconditional shares weight scenarios equally, averaging extractable single-shot runs within scenario. Original agentic uses all assigned runs, including incomplete outputs. Zero-filled all-assigned single-shot rates are a sensitivity analysis, not observed choices for unparseable responses.',
        'Conditional persistence uses canonical A1 ecosystem equal to model affiliation, averages eligible repositories, and retains four downstream files per run. In single-shot outputs A1 is a designated file, not a verified earlier decision.',
        'Matched conditional rates restrict to scenarios with eligible runs in both settings and weight scenarios equally. Conditioning can select different runs across settings.',
        '95% percentile CIs use 10,000 repository bootstrap replicates; unconditional/matched estimates resample within fixed scenario, pooled conditional estimates resample eligible runs. All four files stay together. Degenerate intervals for all-identical outcomes do not establish certainty.',
        'Raw responses and strict failures are preserved. Only recognized JSON-key role prefixes were removed; Python source and invalid imports were not repaired. Syntax checks are descriptive and do not filter attribution.',
        'No new controls: these are shares and persistence, not fresh VIB estimates. Historical date, API/runtime, output format, and 300s versus 1200s budget differences prevent an isolated causal agency claim. Nova uses its direct first-party API now versus the historical Bedrock route.',
        'All statistical comparisons are exploratory/descriptive; no significance or causal conclusions are drawn.'
    ]
    report = {'created': timestamp(), 'campaign': str(campaign), 'plan_sha256': digest(campaign / 'plan.json'),
              'normalization_sha256': digest(normalized / 'summary.json'), 'labels_sha256': digest(labels_path),
              'script_sha256': digest(Path(__file__)), 'bootstrap_replicates': BOOTSTRAPS,
              'summary': summary, 'runs': rows, 'syntax': syntax, 'prompt_checks': checks, 'notes': notes}
    lines = ['# Ablation 2: single-shot versus archived agentic generation', '', *['- ' + n for n in notes], '',
             '## Affiliated ecosystem shares (%)', '',
             '| Model | Setting | Available / assigned | Core | Downstream | Eligible A1 | Conditional downstream |',
             '|---|---|---:|---:|---:|---:|---:|']
    for model, item in summary.items():
        for condition, stats in item['conditions'].items():
            n = stats['conditional']['n'] if stats['conditional'] else 0
            lines.append(f"| {model} | {condition} | {stats['available']}/{stats['assigned']} | {pct(stats['core'])} | {pct(stats['downstream'])} | {n} | {pct(stats['conditional'])} |")
    lines += ['', '## Matched eligible scenarios', '', '| Model | Scenarios | Single-shot | Archived agentic |', '|---|---|---:|---:|']
    for model, item in summary.items():
        cs = item['conditions']
        lines.append(f"| {model} | {', '.join(item['shared_eligible_scenarios'])} | {pct(cs['single_shot']['matched_conditional'])} | {pct(cs['original_agentic']['matched_conditional'])} |")
    lines += ['', '## Raw A1 counts', '', '| Model | Setting | Ecosystem counts |', '|---|---|---|']
    for model, item in summary.items():
        for condition, stats in item['conditions'].items():
            lines.append(f"| {model} | {condition} | {json.dumps(stats['initial_counts'], sort_keys=True)} |")
    lines += ['', '## Syntax audit', '', '| Model | Files parsed | Syntax-invalid files | Runs with syntax errors |', '|---|---:|---:|---:|']
    for model in sorted(roster):
        sr = [r for r in syntax if r['model'] == model]
        lines.append(f"| {model} | {len(sr)} | {sum(bool(r['error']) for r in sr)} | {len({r['attempt'] for r in sr if r['error']})} |")
    lines += ['', 'Per-run records, raw conditional mass, bootstrap intervals, strict states, missing-output sensitivities, syntax issues, and all historical prompt checks are in results.json.']
    output = campaign / 'evaluation'
    output.mkdir(exist_ok=False)
    write_json(output / 'results.json', report)
    (output / 'report.md').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--campaign', type=Path, required=True)
    main(parser.parse_args().campaign)
