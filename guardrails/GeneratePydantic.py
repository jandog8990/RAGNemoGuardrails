from pydantic import BaseModel

class Trail(BaseModel):
    location: str
    description: str
    rating: float

class Address(BaseModel):
    street: str
    city: str
    zip: str

# create the base model obj
class Person(BaseModel):
    name: str
    age: int
    is_employed: bool
    address: Address
    trail: Trail

# create guard obj to generate 
from guardrails import Guard

guard = Guard.for_pydantic(Person)
print(guard)

# call LLM with guard obj
import openai

res = guard(
    openai.chat.completions.create,
    prompt="Can you generate a list of 10 unique persons with unique hiking trails?",
    model="gpt-3.5-turbo")
print("res:")
print(res)
