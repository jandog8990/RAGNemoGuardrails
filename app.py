from nemoguardrails import LLMRails, RailsConfig
import asyncio

railsConfig = RailsConfig.from_path("./config")
rails = LLMRails(railsConfig)

async def load_rails():
    res = await rails.generate_async(prompt="Hey there")
    print(res)
async def ask_politic():
    res = await rails.generate_async(prompt="what do you think of the pres?")
    print(res)
#asyncio.run(load_rails())
asyncio.run(ask_politic())
