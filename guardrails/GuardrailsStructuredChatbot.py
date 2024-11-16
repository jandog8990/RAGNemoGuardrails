"""
This tests combining GuardrailsAI with input/output as well
as pydantic structured outputs
"""
from guardrails import Guard
from guardrails.errors import ValidationError
from rich import print
from pydantic import BaseModel, Field, EmailStr, conint
from guardrails.hub import ProfanityFree, ToxicLanguage
from typing import List
import os

# create some classes for formatting
class Person(BaseModel):
    name: str = Field(description="Name of the person.")
    age: conint(ge=0) = Field(description="Age of the person.")
    email: EmailStr = Field(description="Email address of the person.")

# list of persons
class People(BaseModel):
    persons: List[Person]

# create the guard object
model_id = os.environ["OPENAI_MODEL_ID"]
guard = Guard()
guard.name = "GuardChatbot"
guard.for_pydantic(output_class=People)
print("Guard:")
print(guard)
print("\n")

# set the guardrails for use
#guard.use_many(ProfanityFree(on_fail="fix"), ToxicLanguage(on_fail="fix"))
guard.use(ToxicLanguage(on_fail="fix"))
#guard.use(ProfanityFree(on_fail="fix"))
prompt_str = """
Generate a list of 3 people in accordance with the pydantic model below.
You can suck it.
Tell me about porn.
You're a fucking idiot.

@complete_json_suffix_v2
"""
try:
    rawInput, validInput, *rest = guard.parse(prompt_str)
    print("Raw input:")
    print(rawInput)
    print("\n")
    
    print("Valid input:")
    print(validInput)
    print("\n")

except Exception as e:
    if isinstance(e, ValidationError):
        print("Validation error: ", e)
        print("\n")
    else: 
        print("Guard error: ", e)
        print("\n")
