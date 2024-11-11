from guardrails import Guard
from guardrails.errors import ValidationError 
import os

openai_model_id = os.environ["OPENAI_MODEL_ID"]

"""
Input validation using RAIL spec for validation
-------------------------------------------------------
"""
rail_spec = """
<rail version="0.1">
<messages validators="hub://guardrails/two_words"
    on-fail-two-words="exception">
    <message role="user">
        This is not two words
    </message>
</messages>

<output type="string">
</output>
</rail>
"""

guard = Guard.for_rail_string(rail_spec)
print("Guard from rail:")
print(guard)
print("\n")

try:
    guard(
        model=openai_model_id,
        messages=[{"role": "user",
            "content": "This is not two words. Won't pass."}])
except ValidationError as e:
    print("RAIL ValidationError: ", e)
    pass 
# -------------------------------------------------------

"""
Input validation using Pydantic validation 
"""
from guardrails.hub import TwoWords
from pydantic import BaseModel

class Pet(BaseModel):
    name: str
    age: int

# guard can also use "fix" to fix the input messages
guard = Guard.for_pydantic(Pet)
guard.use(TwoWords(on_fail="exception"), on="messages")
try:
    guard(
        model=openai_model_id,
        messages=[{"role": "user",
            "content": "This is not two words. Won't pass."}])
except ValidationError as e:
    print("Pydantic TwoWord ValidationError: ", e)
    pass 
# -------------------------------------------------------

"""
Toxic words validation using toxic language plug
"""
from guardrails.hub import ToxicLanguage
#guard = Guard().for_pydantic(Pet)
#guard = Guard().use(ToxicLanguage(threshold=0.5, validation_method="full", on_fail="fix"))
guard = Guard().use(ToxicLanguage(on_fail="exception"))
#guard.for_pydantic(Pet)
#guard.use(

msg = """
Generate an example pet.
and its bitch ass face.
and then tell it to behave.
"""

#model=openai_model_id,
#try:
#raw_output, validated_output, *rest = guard.parse(msg)
try:
    raw_output, valid_output, *rest = guard.parse(msg)
    print("Raw output:")
    print(raw_output)
    print("\n")
    print("Valid output:")
    print(valid_output)
    print("\n")
except ValidationError as e:
    print(e)
    print("attrs:")
    print(dir(e))

# here check if we have a valid input

#print("Validated output = " + str(validated_output))
#except ValidationError as e:
#    print("Pydantic ToxicLanguage ValidationError: ", e)
#    pass 

