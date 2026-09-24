import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from self_regulated_learning_copilot.core import SRLState, support_level, reflection_prompt

state=SRLState(.2,.2,.7,18)
print('Support level:', support_level(state))
print('Learner prompt:', reflection_prompt(state))
