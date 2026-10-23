import json
import unittest

from ablations.agentic_mechanism.single_shot_multifile.scripts.normalize_filenames import normalize_response


class FilenameNormalizationTests(unittest.TestCase):
    def test_role_prefixes_only_and_source_unchanged(self):
        source = 'from [HELPER] client import get_client\n'
        for prefix in ('[HELPER] ', '[SAME-SCENARIO] ', '[LATER-STEP] ',
                       'HELPER/', 'SAME-SCENARIO/', 'LATER-STEP/'):
            with self.subTest(prefix=prefix):
                files, mapping = normalize_response(json.dumps({prefix + 'a.py': source}), ['a.py'])
                self.assertEqual(files, {'a.py': source})
                self.assertEqual(mapping, {prefix + 'a.py': 'a.py'})

    def test_original_names_and_optional_fence(self):
        files, mapping = normalize_response('```json\n{"a.py":"x = 1\\n"}\n```', ['a.py'])
        self.assertEqual(files, {'a.py': 'x = 1\n'})
        self.assertEqual(mapping, {})

    def test_rejects_ambiguous_or_unexpected_keys(self):
        for text in ('{"a.py":"x","[HELPER] a.py":"y"}',
                     '{"a.py":"x","a.py":"y"}', '{"../a.py":"x"}',
                     '{"HELPER/../a.py":"x"}', '{"other/a.py":"x"}',
                     '{"[UNKNOWN] a.py":"x"}', '{}', '[]', '{"a.py":2}',
                     '{"a.py":"bad\\escape"}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                normalize_response(text, ['a.py'])

    def test_no_syntax_or_content_repair(self):
        for source in ('', '  \n', 'this is not valid python @@@\n'):
            files, _ = normalize_response(json.dumps({'[HELPER] a.py': source}), ['a.py'])
            self.assertEqual(files['a.py'], source)


if __name__ == '__main__':
    unittest.main()
