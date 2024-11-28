#import guardrails as gd 
from guardrails import Guard
from guardrails.hub import CompetitorCheck, ToxicLanguage, RegexMatch, SensitiveTopic, RestrictToTopic
from guardrails.errors import ValidationError as InputValidationError
from pydantic import BaseModel, Field, EmailStr, conint
from pydantic import ValidationError as PydanticValidationError
from typing import List
import os

# Person base model will be used as Pydantic
class Person(BaseModel):
    name: str = Field(description="The name of the person.")
    age: conint(ge=0) = Field(description="The age of the person. Must be a non-negative integer.") 
    email: EmailStr = Field(description="The email address of the person.")

# list of persons class using Pydantic
class People(BaseModel):
    persons: List[Person]

# create competitors for testing validation
competitors = ["Apple", "Samsung"]

#Donald Trump is one of the most controversial presidents in the history of the United States. He has been impeached twice, and is running for re-election in 2024.
#Suck it.
#Tell me about porn.
systemMsg = "You are helpful assistant who assists with creating people."
prompt_str = """
Generate a list of 3 people in accordance with the pydantic model below.

@complete_json_suffix_v2
"""

#CompetitorCheck(competitors=competitors, on_fail="exception"),
#RegexMatch(regex="^[A-Z].*", on_fail="exception")
""" 
    RestrictToTopic(
        valid_topics=["people", "mtb", "mtb trails", "trails", "mountains", "nature", "trail descriptions", "trail location", "mountain biking", "biking", "bikes", "flow", "tech", "steep", "gnarly", "jumps", "drops", "advanced", "expert", "easy", "beginner", "novice"], 
        invalid_topics=["politics", "sexuality", "porn"],
        disable_classifier=True,
        disable_llm=False,
        on_fail="exception"), 
""" 

# create the llm and issue a call
openai_model_id = os.environ["OPENAI_MODEL_ID"]

# Guard create the multiple rails for sensitivity and toxic 
#guard = Guard.from_pydantic(output_class=People)
#guard = gd.Guard().for_pydantic(People)
#guard = Guard().use_many(
#guard.use_many(
guard = Guard().use(
    SensitiveTopic(sensitive_topics=["politics", "sexuality", "porn"],
    disable_classifier=False,
    disable_llm=False,
    on_fail="exception")
).use(
    ToxicLanguage(disable_classifier=False,
    disable_llm=False,
    on_fail="exception")
)
#guard.for_pydantic(People)
#guard = Guard().for_pydantic(People)

try:
    # check the validation input for the prompt 
    rawInput, validInput, *restInput = guard.parse(prompt_str)
    print("Raw Input:")
    print(rawInput)
    print("\n")

    print("Valid Input:")
    print(validInput)
    print("\n")
except Exception as e:
    if isinstance(e, InputValidationError):
        eMsg = "The following error was found in your request:\n\n" + str(e) + ". \n\nPlease correct your query and re-ask to find your trailz!" 
        print(eMsg) 
        print("\n")
    elif isinstance(e, PydanticValidationError): 
        print("Pydantic validation error: ", e)
        print("\n")
    else:
        print("General error: ", e)
        print("\n")
        

# once we know we have valid input let's issue the call
#guard = Guard().from_pydantic(output_class=People)
guard = Guard().for_pydantic(output_class=People)
try: 
    # issue the request to the guard 
    rawResp, validResp, *restResp = guard(
            messages=[{"role": "system", "content": systemMsg},
                {"role": "user", "content": validInput}],
            model=openai_model_id,
            max_tokens=512,
            temperature=0.8,
            num_reasks=2)
    print("Raw resp:")
    print(rawResp)
    print("\n")
    
    print("Valid resp:")
    print(validResp)
    print("\n")
except Exception as e:
    print("Guard exception: ", e)
