"""Check pinned BMad files and two observable helper behaviors; no network."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent
manifest = json.loads((ROOT / 'docs/bmad-files.json').read_text(encoding='utf-8-sig'))
for entry in manifest['files']:
    actual = hashlib.sha256((ROOT / entry['path']).read_bytes()).hexdigest()
    if actual != entry['sha256']:
        raise SystemExit(f"Source mismatch: {entry['path']}")

kit = ROOT / 'skills/bmad-deep-recon/scripts/recon_kit.py'


def run(*args):
    result = subprocess.run([sys.executable, str(kit), *map(str, args)],
                            capture_output=True, encoding='utf-8')
    if result.returncode != 1:
        raise SystemExit(f'Expected detected issue, got {result.returncode}: {result.stderr}')
    return json.loads(result.stdout)


citations = run('citations', FIXTURES / 'incomplete-report.md')
assert citations['dangling_markers'] == [4], citations
assert citations['orphaned_rows'] == [3], citations
staleness = run('staleness', FIXTURES / 'fictional-claims.json',
                '--windows', '{"pricing":3}', '--today', '2026-10-23')
assert staleness['stale_count'] == 1, staleness
assert [x['stale'] for x in staleness['claims']] == [True, False], staleness
print(json.dumps({'unchanged_upstream_files': len(manifest['files']),
                  'missing_and_unused_citations': 'pass', 'stale_price': 'pass'}))
