from pydantic import BaseModel, Field, EmailStr, conint, ValidationError
from guardrails import Guard
from typing import List
#from guardrails.utils import read_rail
from openai import OpenAI

# Person base model will be used as Pydantic 
class Person(BaseModel):
    name: str = Field(description="The name of the person.")
    age: conint(ge=0) = Field(description="The age of the person. Must be a non-negative integer.")
    email: EmailStr = Field(description="The email address of the person.")

# list of persons class using Pydantic
class People(BaseModel):
    persons: List[Person]

rail_spec = """
<rail version="0.1">
    <output>
        <list name="people" description="A list of 3 people.">
            <pydantic model="Person" on-fail-pydantic="reask"/>
        </list>
    </output>
    <prompt>
        Generate data for possible users in accordance with the pydantic model below.

        @complete_json_suffix_v2
    </prompt>
</rail>
"""

# create the llm and issue a call
import openai
import os
#openai_key = os.environ["OPENAI_API_KEY"]
#openai_client = OpenAI(api_key=openai_key) 
openai_model_id = os.environ["OPENAI_MODEL_ID"]
#guard = Guard.from_rail_string(rail_spec)
guard = Guard.for_pydantic(People)
        #llm_api=openai.completions.create, 
        #model=openai_client, 
#validated_response = guard(
#openai.chat.completions.create, 
prompt_str = """
Generate a list of 3 people in accordance with the pydantic model below.

@complete_json_suffix_v2
"""
#prompt_str = "Generate a list of 3 possible users" 
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
