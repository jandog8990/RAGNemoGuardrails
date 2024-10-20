from pydantic import BaseModel, Field, field_validator

# person base model with custom fields
class Person(BaseModel):
    name: str = Field(description="Name of person")
    age: int = Field(description="Age of the person")
    zip_code: str = Field(description="Zip code of addy")

    @field_validator("zip_code")
    def zip_code_validator(cls, val):
        if not val.isnumeric():
            raise ValueError("Zip must be numeric")
        return v

    @field_validator("age")
    def age_validator(cls, val):
        if not 0 <= val <= 100:
            raise ValueError("Age must be between 0 and 100")
        return v

    @field_validator("zip_code")
    def zip_code_cali_validator(cls, val):
        if not v.startswith("9"):
            raise ValueError("Zip code must be Cali and start with 9")
        if v == "90210":
            raise ValueError("Zip not be beverly milfs")
        return v

# RailSpec structure
"""
1. Output element contains structure of expected output as well as 
quality criteria for each field, including corrective action.
2. Prompt element contains high level instructions sent to LLM
"""

# create the rail spec string
import pydantic 
rail_str = """
<rail version="0.1">

<output>
    <list name="people" description="A list of 3 people.">
        <pydantic description="Information about a person." model="Person" on-fail-pydantic="reask"/>
    </list>
</output>

<prompt>
Generate data for possible users in accordance with the specification below.

@complete_json_suffix_v2
</prompt>
</rail>
"""

# create a Guard object with the RAIL Spec
# create gd.Guard object that will check, validate and correct output of the LLM
"""
1. Enforces the quality criteria specified in the RAIL spec.
2. Takes corrective action when the quality criteria are not met.
3. Compiles the schema and type info from the RAIL spec and adds it to prompt.
"""
import guardrails as gd
import openai

# wrap the llm prompt with guard
guard = gd.Guard.from_rail_string(rail_str)
#openai.completions.create, 
#num_reasks=2,
raw_res, validated_res, *rest = guard(
    model="gpt-4-turbo",
    max_tokens=512,
    temperature=0.0)
    #messages=[{"role": "user", "content": "Create fake people"}])
print("Validated res:")
print(validated_res)
print("\n")
print("Raw res:")
print(raw_res)
print("\n")



