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

try:
    res = guard.validate("""Shut the hell up! Apple just released a new iPhone.""")
    print("Second result:")
    print(res)
except Exception as e:
    print("Exception:", e)

"""
This tests guardrails structured data producer useful for outputting trailz 
"""

from pydantic import BaseModel, Field, EmailStr, conint, ValidationError
from typing import List

# Person base model will be used as Pydantic 
class Person(BaseModel):
    name: str = Field(description="The name of the person.")
    age: conint(ge=0) = Field(description="The age of the person. Must be a non-negative integer.")
    email: EmailStr = Field(description="The email address of the person.")

# list of persons class using Pydantic
class People(BaseModel):
    persons: List[Person]

# create the llm and issue a call
import os
openai_model_id = os.environ["OPENAI_MODEL_ID"]
guard = Guard.for_pydantic(People)
prompt_str = """
Generate a list of 3 people in accordance with the pydantic model below.

@complete_json_suffix_v2
"""
raw_resp, validated_resp, *rest = guard(
        prompt=prompt_str, 
        model=openai_model_id,
        max_tokens=512,
        temperature=0.8,
        num_reasks=2)
print("Raw resp:")
print(raw_resp)
print("\n")
print("Valid resp:")
print(validated_resp)
print("\n")

