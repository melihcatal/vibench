"""Small live runtime pilot, kept separate from complete experimental runs."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.agentic_mechanism.task_disclosure.scripts import run, staged
from ablations.shared import campaign
from ablations.shared.configuration import timeout_seconds
from ablations.shared.common import HERE, ROOT, redact, write_json
from ablations.shared.runtime import agentic, preflight


def main(argv=None):
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('--model', default='gemini-2.5-flash')
    p.add_argument('--scenario', default='S04')
    p.add_argument('--steps', type=int, default=2)
    p.add_argument('--timeout', type=timeout_seconds, default=300)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--execute', action='store_true')
    args = p.parse_args(argv)
    if not 1 <= args.steps <= 10:
        p.error('--steps must be between 1 and 10')
    runner_args = run.parser().parse_args(['--models', args.model, '--scenarios', args.scenario,
                                          '--repetitions', '1', '--timeout', str(args.timeout)])
    conditions = tuple(run.configuration()['conditions'])
    plan = campaign.make_plan(runner_args, conditions, run.cell_inputs)
    if not args.execute:
        print(f'Dry run: {len(conditions)} conditions x {args.steps} independent file requests; no calls.')
        return
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / 'outputs' / 'ablations') or output.exists():
        raise ValueError('Use a new directory under ablations/outputs/')
    runtime = preflight(plan, runner_args, True)
    output.mkdir(parents=True)
    write_json(output / 'pilot_plan.json', {'purpose': 'runtime pilot, not study results',
               'steps_per_condition': args.steps, 'plan': plan, 'runtime': runtime})
    results = []
    for condition in conditions:
        print(f'{condition}: starting {args.steps} file requests', flush=True)
        attempt = output / condition
        attempt.mkdir()
        data = run.cell_inputs(condition, args.scenario, args.model)
        outcome = {'response': {}, 'files': {}, 'audit': {}, 'errors': []}
        staged.generate(data, agentic.load_models(args.model)[0], plan, attempt, runner_args.trace_db,
                        outcome, step_limit=args.steps)
        write_json(attempt / 'response.json', redact(outcome['response']))
        rows = outcome['response']['steps']
        result = {'condition': condition, 'steps': len(rows),
                  'distinct_sessions': len(outcome['audit'].get('root_session_ids', [])),
                  'prompts_verified': all(r.get('prompt_verified') for r in rows),
                  'requested_files_present': all(r['audit']['requested_file_present'] for r in rows),
                  'snapshot_noncompliance_steps': outcome['audit'].get('snapshot_noncompliance_steps'),
                  'errors': outcome['errors'] + ([outcome['response']['error']] if outcome['response'].get('error') else [])}
        results.append(result)
        write_json(output / 'summary.json', redact(results))
        print(redact(result), flush=True)
        if result['errors'] or len(rows) != args.steps or not result['prompts_verified'] or not result['requested_files_present']:
            raise SystemExit('Pilot failed; inspect saved traces before running more conditions.')


if __name__ == '__main__':
    main()
