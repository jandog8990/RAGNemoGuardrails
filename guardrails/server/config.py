from guardrails import Guard
from guardrails.hub import TwoWords
guard = Guard()
guard.name = 'two-word-guard'
print("GUARD PARAMETERS UNFILLED! UPDATE THIS FILE!")  # TODO: Remove this when parameters are filled.
guard.use(TwoWords())  # TODO: Add parameters.