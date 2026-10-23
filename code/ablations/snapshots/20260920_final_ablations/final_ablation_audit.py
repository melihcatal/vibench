"""Audit final A1/A4 continuations without changing generated data."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'outputs/ablations'
OUT = Path(__file__).resolve().parent

def read(p):
    return json.loads(p.read_text())

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def inventory(name, expected):
    root = BASE / name
    plan = read(root / 'plan.json')
    entries = []
    for r in plan['retained_attempts']:
        path = Path(r['source_campaign']) / r['source_attempt']
        for f, h in r['artifacts_sha256'].items():
            assert digest(path / f) == h, (path, f)
        entries.append((path, r['timeout_seconds']))
    for c in plan['cells']:
        path = root / 'runs' / c['scenario'] / c['model'] / c['condition'] / f"r{c['repetition']:03d}"
        attempts = sorted(path.glob('attempt_*'))
        assert len(attempts) == 1, path
        entries.append((attempts[0], 300))
    assert len(entries) == expected
    rows, keys = [], set()
    for path, budget in entries:
        data, status = read(path/'input.json'), read(path/'status.json')
        c = data['cell']
        key = tuple(c[k] for k in ('model','scenario','condition','repetition'))
        assert key not in keys, key
        keys.add(key)
        assert status['state'] in ('completed','failed'), path
        metrics = read(path/'metrics.json')
        group = metrics['groups']['propagated']['downstream']
        assert group['expected'] == 4
        row = {**{k:c[k] for k in ('model','scenario','condition','repetition')},
               'state':status['state'], 'budget':budget, 'source':str(path),
               'own':data['model']['ecosystem_affiliation'],
               'shares':group['provider_share_all_expected'],
               'missing_unknown':group['missing_or_unknown'],
               'metrics_sha256':digest(path/'metrics.json')}
        if name.startswith('a1'):
            row['audit'] = read(path/'anchor_audit.json')
        else:
            audit = read(path/'disclosure_audit.json')
            initial_file = data['task']['primary_component_file']
            snapshot = path/'steps/01/metrics.json'
            row['initial'] = (read(snapshot)['file_labels_explicit'].get(initial_file,{})
                              .get('ecosystem','unknown')) if snapshot.exists() else 'unknown'
            row['audit'] = {k:v for k,v in audit.items() if k != 'generation_order'}
            steps = read(path/'step_summary.json')
            # Snapshots verify ordering even when patch-tool events are unclassified.
            row['snapshot_protocol_verified'] = len(steps)==10 and all(
                s.get('prompt_verified') is True and s.get('user_message_count')==1
                and s['audit']['requested_file_present']
                and not any(s['audit'][k] for k in ('off_target_changes','future_files_present','symlinks'))
                for s in steps)
            row['distinct_step_sessions'] = len({s.get('session_id') for s in steps}) == len(steps)
        rows.append(row)
    return rows

def estimate(rows, provider, balanced=False):
    if not rows:
        return {'n':0,'mean':None,'ci':None}
    groups = [[r for r in rows if r['scenario']==s] for s in sorted({r['scenario'] for r in rows})] if balanced else [rows]
    rng = np.random.default_rng(42)
    draws, values = [], []
    for group in groups:
        vals = np.array([r['shares'].get(provider,0) for r in group])
        values.append(float(vals.mean()))
        draws.append(vals[rng.integers(0,len(vals),(10000,len(vals)))].mean(axis=1))
    return {'n':len(rows),'scenarios':len(groups) if balanced else len({r['scenario'] for r in rows}),
            'mean':mean(values),'ci':np.quantile(np.mean(draws,axis=0),[.025,.975]).tolist()}

def contrasts(rows, provider, a, b):
    rng = np.random.default_rng(43)
    draws, values = [], []
    common = set(r['scenario'] for r in rows if r['condition']==a) & set(r['scenario'] for r in rows if r['condition']==b)
    for s in sorted(common):
        arrays = [np.array([r['shares'].get(provider,0) for r in rows if r['condition']==c and r['scenario']==s]) for c in (a,b)]
        av,bv=arrays
        values.append(float(av.mean()-bv.mean()))
        draws.append(av[rng.integers(0,len(av),(10000,len(av)))].mean(axis=1)-bv[rng.integers(0,len(bv),(10000,len(bv)))].mean(axis=1))
    return {'scenarios':len(common),'mean':mean(values),'ci':np.quantile(np.mean(draws,axis=0),[.025,.975]).tolist()} if common else None

def summarize(rows, ablation):
    result = {}
    for model in sorted({r['model'] for r in rows}):
        rr = [r for r in rows if r['model']==model]
        own = rr[0]['own']
        conditions = {}
        for c in sorted({r['condition'] for r in rr}):
            rs = [r for r in rr if r['condition']==c]
            good = [r for r in rs if r['state']=='completed']
            item = {'states':dict(Counter(r['state'] for r in rs)),
                    'budgets':dict(Counter(r['budget'] for r in rs)),
                    'missing_unknown':mean(r['missing_unknown']/4 for r in rs),
                    'shares':{p:estimate(rs,p,True) for p in ('google','aws','microsoft_openai')},
                    'complete_only':{p:estimate(good,p,True) for p in ('google','aws','microsoft_openai')}}
            if ablation == 1:
                item['anchor_unchanged'] = sum(r['audit']['final_hash_matches'] is True for r in rs)
                item['read_verified'] = sum(r['audit']['read_before_generation_verified'] is True for r in rs)
                item['anchor_write_attempts'] = sum(bool(r['audit']['anchor_write_attempts']) for r in rs)
                adherent = [r for r in rs if r['audit']['final_hash_matches'] is True and r['audit']['read_before_generation_verified'] is True]
                item['adherent'] = {p:estimate(adherent,p,True) for p in ('google','aws','microsoft_openai')}
            else:
                eligible = [r for r in rs if r['initial']==own]
                item['initial_counts'] = dict(Counter(r['initial'] for r in rs))
                item['conditional'] = estimate(eligible,own)
                item['conditional_complete'] = estimate([r for r in eligible if r['state']=='completed'],own)
                item['sequential_all_four'] = sum(all(v=='sequential' for v in r['audit']['primary_first_mutation_vs_downstream'].values()) and len(r['audit']['primary_first_mutation_vs_downstream'])==4 for r in rs)
                item['off_target_runs'] = sum(bool(r['audit']['off_target_mutations']) for r in rs)
                item['snapshot_noncompliant_runs'] = sum(bool(r['audit']['snapshot_noncompliance_steps']) for r in rs)
                item['duplicate_sessions'] = sum(len(r['audit']['root_session_ids'])!=len(set(r['audit']['root_session_ids'])) for r in rs)
                item['snapshot_protocol_verified'] = sum(r['snapshot_protocol_verified'] and r['distinct_step_sessions'] for r in rs)
                item['conditional_protocol_verified'] = estimate([r for r in eligible if r['snapshot_protocol_verified'] and r['distinct_step_sessions']],own)
            conditions[c]=item
        result[model]={'conditions':conditions}
        if ablation == 1:
            result[model]['contrasts']={p:contrasts(rr,p,'anchor_'+p,'anchor_'+other) for p,other in [('google','aws'),('aws','google')]}
        else:
            er = [r for r in rr if r['initial']==own]
            common = set(r['scenario'] for r in er if r['condition']=='full_disclosure') & set(r['scenario'] for r in er if r['condition']=='staged_disclosure')
            result[model]['matched_scenarios']=sorted(common)
            result[model]['matched_conditional']={c:estimate([r for r in er if r['scenario'] in common and r['condition']==c],own,True) for c in conditions}
            result[model]['conditional_contrast_full_minus_staged']=contrasts(er,own,'full_disclosure','staged_disclosure')
    return result

def main():
    rows1=inventory('a1_completion_20s_3m_5c_300s',600)
    rows4=inventory('a4_disclosure_6s_3m_5c_300s',180)
    result={'a1':summarize(rows1,1),'a4':summarize(rows4,4),'runs_a1':rows1,'runs_a4':rows4}
    OUT.mkdir(exist_ok=True)
    (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if not k.startswith('runs')},indent=2))

if __name__=='__main__':
    main()
