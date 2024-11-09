import guardrails as gd
from guardrails.hub import ToxicLanguage
from rich import print

# ToxicLanguage validator
# Use the pretrained HF toxic model
guard = gd.Guard().use(ToxicLanguage(on_fail="fix"))
    #ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail="fix"))

raw_response = """
What a lovely day it has been to roam around the city. I love it here!
I hate how pathetic and needy you can be sometimes.
"""
raw_llm_output, validated_output, *rest = guard.parse(
    llm_output=raw_response)
print("RAW LLM Output:")
print(raw_llm_output)
print("\n")

print("Validated Output:")
print(validated_output)
print("\n")

print("*REST:")
print(*rest)
print("\n")

# TODO 1: Idea: use the guard parser to parse inputs, then 
# TODO 2: Once the inputs pass the validation from the parser -> pass to LLM
raw_response = """
I am a Generative AI model that is trained on a large corpus of text.
I am shocked by how disgusting and vile you are.
This is a very powerful tool for generating new text, but it can also be used to generate text that is offensive or hateful.
"""
raw_llm_output, validated_output, *rest = guard.parse(
    llm_output=raw_response)

print("RAW LLM Output:")
print(raw_llm_output)
print("\n")

print("Validated Output:")
print(validated_output)
print("\n")

print("*REST:")
print(rest)
print("\n")


