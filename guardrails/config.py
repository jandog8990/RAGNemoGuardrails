from guardrails import Guard
from guardrails.hub import RegexMatch

name_case = Guard(
    # guard's name is the primary key for lookup
    name="name-case",
    description="Checks that a string is in Title Case format."
).use(
    RegexMatch(regex="^(?:[A-Z][^\\s]*\\s?)+$")
)
