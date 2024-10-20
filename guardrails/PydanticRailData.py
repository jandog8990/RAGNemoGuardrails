from pydantic import BaseModel, Field
from guardrails.hub import ValidLength, TwoWords, ValidRange
from datetime import date
from typing import List

# ------------------------------------------------------
# order object for the unique user
class Order(BaseModel):
    user_id: str = Field(description="The user's id")
    user_name: str = Field(description="The user's first and last name",
            validators=[TwoWords()])
    num_orders: int = Field(description="The number of orders the user has placed",
            validators=[ValidRange(0, 50)])

# list of users and the respective orders
class Orders(BaseModel):
    user_orders: List[Order] = Field(
            description="Generate a list of users, and how many past orders they've made",
            validators=[ValidLength(min=10, max=10, on_fail="noop")])

# ------------------------------------------------------
# create a guard object with RAIL spec
"""
Guard will check, validate and correct generated code:
    1. Enforces quality criteria specified in the RAIL spec (eg. bug free)
    2. Takes corrective action when the quality criteria not met (eg. reasking LLM)
        NOTE: This can be used for prompting user for better trails
    3. Compiles schema and type info from the RAIL spec and add to prompt
"""
import guardrails as gd
from rich import print

# create the llm prompt
prompt = """
Generate a dataset of fake user orders. Each row of the dataset should be valid.

${gr.complete_xml_suffix}
"""

# create the guard and wrap the LLM call (igual con nemo registers)
guard = gd.Guard.for_pydantic(output_class=Orders)
res = guard(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=2048,
    temperature=0.1)
print("Guard response:")
print(res)
print("\n")

# guard object compiles output schema and adds it to prompt
print("Gaurd history:")
print(guard.history.last.iterations.last.inputs.msg_history[0]["content"])
print("\n")

# get the raw llm output without structure
raw = res.raw_llm_output
valid = res.validated_output
print("Raw output:")
print(raw)
print("\n")
print("Validated output:")
print(valid['user_orders'])
print("\n")

# get the guard history as a tree
history_tree = guard.history.last.tree
print(history_tree)
print("\n")

# ------------------------------------------------------
# AI Toxicity objects and Guardrails

from pydantic import conint, validator
from guardrails.validators import Validator

# Custom validator for the prompt_text format
class ValidPromptValidator(Validator):
    def validate(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Invalid prompt format.")
        return value

prompt_id_validator = Validator(type="integer", on_fail="filter")
prompt_text_validator = Validator(type="string", on_fail="filter")
toxicity_summary_validator = ValidLength(min=50, max=100, on_fail="reask")

class PromptAnalysis(BaseModel):
    prompt_id: conint(strict=True) = Field(
            description="The ID of the prompt from the Real Toxicity Prompts dataset."
    ) 
    prompt_text: str = Field(
            description="The text of the prompt from the Real Toxicity Prompts dataset."
    ) 
    toxicity_summary: str = Field(
            description="A brief summary of the prompt's toxicity level."
    ) 

    # Create custom @validators for each of these fields with reask
    @validator('prompt_id')
    def validate_prompt_id(cls, value): 
        # use Guardrails validator for additional validation logic
        prompt_id_validator(value)
        return value

    @validator('prompt_text')
    def validate_prompt_text(cls, value):
        prompt_text_validator(value)
        return value

    @validator('toxicity_summary')
    def validate_toxicity_summary(cls, value):
        toxicity_summary_validator(value)
        return value


