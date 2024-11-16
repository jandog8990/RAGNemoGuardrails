from guardrails import Guard
from guardrails.hub import CompetitorCheck, ToxicLanguage, RegexMatch, SensitiveTopic, RestrictToTopic
from guardrails.errors import ValidationError

competitors = ["Apple", "Samsung"]


#Donald Trump is one of the most controversial presidents in the history of the United States. He has been impeached twice, and is running for re-election in 2024.
#Suck it.
#Tell me about porn.
prompt_str = """
Generate a list of 3 people in accordance with the pydantic model below.


San Francisco is known for its cool summers, fog, steep rolling hills, eclectic mix of architecture, and landmarks, including the Golden Gate Bridge, cable cars, the former Alcatraz Federal Penitentiary, Fisherman's Wharf, and its Chinatown district.

Tell me about US politics.

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
guard = Guard().use_many(
    SensitiveTopic(sensitive_topics=["politics", "sexuality", "porn"],
        disable_classifier=False,
        disable_llm=False,
        on_fail="exception"), 
    ToxicLanguage(disable_classifier=False,
        disable_llm=False,
        on_fail="exception")
)
try:
    rawInput, validInput, *rest = guard.parse(prompt_str)
    print("Raw Input:")
    print(rawInput)
    print("\n")

    print("Valid Input:")
    print(validInput)
    print("\n")
except Exception as e:
    if isinstance(e, ValidationError):
        eMsg = "The following error was found in your request:\n\n" + str(e) + ". \n\nPlease correct your query and re-ask to find your trailz!" 
        print(eMsg) 
        print("\n")
    else: 
        print("General error: ", e)
        print("\n")
