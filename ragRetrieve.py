import os
from openai import OpenAI
from pinecone import Pinecone
from tqdm.auto import tqdm
from nemoguardrails import LLMRails, RailsConfig
import asyncio

"""
RAG Retrieve uses PineCone and NemoGuardrails to generate
data by using textual information queried from PineCone db
"""

# get the env variables for openai and PC
indexName = "nemo-guard-rag-test"
openai_api_key = os.environ["OPENAI_API_KEY"]
pc_api_key = os.environ["PINE_CONE_API_KEY"]
openai_model_id = os.environ["OPENAI_MODEL_ID"]

# create the OpenAI client 
client = OpenAI(api_key=openai_api_key)

# create the PC index
pc = Pinecone(api_key=pc_api_key)
index = pc.Index(indexName)

# create the retrieve function for PC using embeddings
async def retrieve(query: str) -> list:
    print("> PC Retrieve called")

    # openai embedding 
    embed_model_id = "text-embedding-3-small"
    res = client.embeddings.create(
        input=query,
        model=embed_model_id
    )
    resData = res.data[0]
    embedding = resData.embedding

    # get the relevant contexts from PC
    res = index.query(
        vector=embedding,
        top_k=5,
        include_metadata=True)
    
    # get the list of retrieved texts from the matches
    contexts = [x['metadata']['chunk'] for x in res['matches']]
    return contexts

# create the RAG retrieval using contexts and given query
async def rag(query: str, contexts: list) -> str:
    print("> RAG Called")
    context_str = "\n".join(contexts)

    # place query and contexts into RAG prompt
    system_msg = "You are a helpful assistant." 
    prompt = f"""You are a helpful assistant, below is a query from a user and
    some relevant contexts. Answer the question given the information in those
    contexts. If you cannot find the answer to the question, say "I don't know".

    Contexts:
    {context_str}

    Prompt: {query}
     
    Answer: """

    # create the messages to send for system/user prompting
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt}
    ]


    # generate the answer using chat streaming
    res = client.chat.completions.create(
        model=openai_model_id,
        messages=messages,
        temperature=0.0,
        max_tokens=100, 
        stream=False
    )

    print("Response rag:")
    print(res)
    print("\n")

    #return stream
    return res['choices'][0]['text']

# create nemoguard rails using config 
railsConfig = RailsConfig.from_path("./ragconfig")
ragRails = LLMRails(config=railsConfig)

# register context and rag actions
ragRails.register_action(action=retrieve, name="retrieve")
ragRails.register_action(action=rag, name="rag")

# try out the rag agent
async def sayHello():
    res = await ragRails.generate_async(prompt="hello")
    print(res)

def askLlama():
    res = ragRails.generate(prompt="tell me about llama 2")
    print(res)

#asyncio.run(askLlama())
askLlama()
