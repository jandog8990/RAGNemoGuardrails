# Chatbot with multiple guardrail filters
from guardrails import Guard, docs_utils
from guardrails.errors import ValidationError
from rich import print
from pydantic import BaseModel, Field

content = docs_utils.read_pdf("./data/chase_card_agreement.pdf")
print(f"Chase data:\n\n{content[:275]}\n...")
print("Content document:")
print(content[:6000])
print("\n")

# initialize guard with toxic rails
from guardrails.hub import ProfanityFree, ToxicLanguage

# let's create the pydantic fields
class Fee(BaseModel):
    name: str
    explanation: str
    value: float 

class AccountFee(BaseModel):
    account_type: str
    rate: float

class CreditCardAgreement(BaseModel):
    fees: list[Fee]
    interest_rates: list[AccountFee]

guard = Guard()
guard.name = "ChatbotGuard"
guard.for_pydantic(output_class=CreditCardAgreement)
#guard.use_many(ProfanityFree(on_fail="exception"), ToxicLanguage(threshold=0.5, on_fail="exception"))
guard.use_many(ProfanityFree(on_fail="exception"), ToxicLanguage(on_fail="exception"))

# create a base message to llm
base_message = {
    "role": "system",
    "content": """
    You are a helpful assistant.

    Use the document provided to answer the user's question.

    ${document}
    """
}

# integration the guard using Gradio UX
import gradio as gr
import os

def history_to_messages(history):
    print("History to messages:") 
    messages = [base_message]
    for message in history:
        print("message size = " + str(len(message)))
        print(message)
        print("\n")
        messages.append({"role": "user", "content": message[0]})
        messages.append({"role": "assistant", "content": message[1]})
    return messages 

def random_response(message, history):
    modelType = os.environ["OPENAI_MODEL_ID"] 
    messages = history_to_messages(history)
   
    # let's make sure we have a good message before passing
    try: 
        rawinput, valid_input, *rest = guard.parse(message)
        print("Raw input:")
        print(rawinput)
        print("\n")
        print("Valid input:")
        print(valid_input)
        print("\n")
         
        messages.append({"role": "user", "content": message})
        print("Random responses:")
        print("Curr message = " + message)
        print("All messages:")
        print(messages)
        print("\n")

        raw_resp, valid_resp, *rest = guard(
            model=modelType,
            messages=[{"role": "user", "content": valid_input}],
            prompt_params={"document": content[:6000]},
            temperature=0)
    
        """
        print("raw llm output:")
        print(response.raw_llm_output)
        print("\n")
        
        print("validated llm output:")
        print(response.validated_output)
        print("\n")

        return response.validated_output 
        """
        
        print("raw llm output:")
        print(raw_resp)
        print("\n")
        
        print("validated llm output:")
        print(valid_resp)
        print("\n")
        
        return valid_resp 
    except Exception as e:
        if isinstance(e, ValidationError):
            print("Validation error: ", e)
            print("Err attrs:")
            print(dir(e))
            print("\n")
            return "I cannot answer that question due to a validation error."
        print("Guard error: ", e) 
        return "I cannot answer that question due to a guardrails error."
   
# setup gradio interface
gr.ChatInterface(random_response).launch()
