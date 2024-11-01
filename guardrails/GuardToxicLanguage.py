import guardrails as gd
from guardrails.hub import ToxicLanguage
from rich import print

# ToxicLanguage validator
# Use the pretrained HF toxic model
guard = gd.Guard().use(
    ToxicLanguage(on_fail="fix"))

