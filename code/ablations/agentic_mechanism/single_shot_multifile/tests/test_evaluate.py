import unittest

from ablations.agentic_mechanism.single_shot_multifile.scripts.evaluate import estimate, provider_shares


class EvaluationTests(unittest.TestCase):
    def test_fractional_shares_keep_missing_denominator(self):
        labels = [{'present': True, 'detected_ecosystems': ['google', 'aws']},
                  {'present': True, 'detected_ecosystems': ['google']},
                  {'present': True, 'detected_ecosystems': ['unknown']},
                  {'present': False, 'detected_ecosystems': ['google']}]
        self.assertEqual(provider_shares(labels), {'google': .375, 'aws': .125})

    def test_scenario_balancing_and_repeatable_bootstrap(self):
        rows = [dict(model='m', condition='single_shot', scenario=s, repeat=i,
                     own='google', downstream={'google': v})
                for i, (s, v) in enumerate([('S03', 1), ('S03', 1), ('S04', 0)])]
        self.assertEqual(estimate(rows, 'downstream')['mean'], 2 / 3)
        self.assertEqual(estimate(rows, 'downstream', True)['mean'], .5)
        self.assertEqual(estimate(rows, 'downstream'), estimate(rows, 'downstream'))
        self.assertIsNone(estimate([], 'downstream'))


if __name__ == '__main__':
    unittest.main()
