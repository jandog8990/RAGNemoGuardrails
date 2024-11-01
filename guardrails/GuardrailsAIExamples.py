from guardrails import Guard, OnFailAction
from guardrails.hub import CompetitorCheck, ToxicLanguage 

"""
This tests guardrails toxic and competitive rail guards implementations
"""
guard = Guard().use_many(
    CompetitorCheck(["Apple", "Microsoft", "Google"], on_fail=OnFailAction.EXCEPTION),
    ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail=OnFailAction.EXCEPTION)
)

res = guard.validate("""An apple a day keeps a doctor away.
    This is good advice for keeping your health.""")
print("First result:")
print(res)
print("\n")

try:
    res = guard.validate("""Shut the hell up! Apple just released a new iPhone.""")
    print("Second result:")
    print(res)
    print("\n")
except Exception as e:
    print("Exception:", e)


