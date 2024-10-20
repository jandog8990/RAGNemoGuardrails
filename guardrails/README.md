## Generating structured data

1. Pydantic: Create pydantic model with desired fields/types, then create Guard object that uses Pydantic model to generate structured data. Finally, call LLM of choice with guard object to generate structured data.

2. RAIL: Create RAIL (xml) spec with desired fields/types. Create Guard obj that uses RAIL spec to generate structured data. Finally, call LLM to generate.


