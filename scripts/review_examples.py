"""Reproduce the labeled worked example; this is not an empirical study."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from self_regulated_learning_copilot import core
outputs={'planning fields present: 3 of 4': 3/4}
result={'kind':'illustrative_calculation','note':'Illustrative structural completeness, not plan quality.','outputs':outputs}
(ROOT/'results/review_examples.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
