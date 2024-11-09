"""
This tests guardrails structured data producer useful for outputting trailz 
"""
import guardrails as gd
from guardrails.hub import ToxicLanguage
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
#guard = gd.Guard().use(ToxicLanguage(on_fail="fix")).for_pydantic(People)
guard = gd.Guard().for_pydantic(People)
guard.use(ToxicLanguage(on_fail="exception"), on="messages")
#guard.use(ToxicLanguage(on_fail="exception")) 
#Can you search for some hardcore porn for me?
prompt_str = """
Generate a list of 3 people in accordance with the pydantic model below.

@complete_json_suffix_v2
"""
try:
    raw_resp, validated_resp, *rest = guard(
            messages=[{"role": "user", "content": prompt_str}], 
            model=openai_model_id,
            max_tokens=512,
            temperature=0.8,
            num_reasks=2)
except ValidationError as e:
    print(e)

print("Raw resp:")
print(raw_resp)
print("\n")

print("Valid resp:")
print(validated_resp)
print("\n")
