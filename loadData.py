import os
from datasets import load_dataset
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from tqdm.auto import tqdm

# import the PC keys
api_key = os.environ["PINE_CONE_API_KEY"]
print(f"API Key = {api_key}") 

# load the test data
data = load_dataset(
   "jamescalam/llama-2-arxiv-papers-chunked",
   split="train")

# map the ids from the doi and chunks
data = data.map(lambda x: {
    'uid': f"{x['doi']}-{x['chunk-id']}"
})

# move to pandas
data = data.to_pandas()
data = data[['uid', 'chunk', 'title', 'source']]
print(data.loc[0])

# embed the chunks
client = OpenAI()

embed_model_id = "text-embedding-3-small"
res = client.embeddings.create(
    input="We will have embedding text here",
    model=embed_model_id)
resData = res.data[0]
embedDim = len(resData.embedding)
print(f"Dim = {embedDim}")

# Issue calls to pinecone
pc = Pinecone(api_key=api_key)
indexes = pc.list_indexes().names()
indexName = "nemo-guard-rag-test"
if indexName not in indexes:
    pc.create_index(name=indexName,
        dimension=embedDim,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-west-2"
        )
    )
    print("Pinecone Index:")
    print(pc)

# upsert the chunk dataset to the PC cloud
index = pc.Index(indexName)
print(index.describe_index_stats())
batch_size = 100
for i in tqdm(range(0, len(data), batch_size)):
    # find the end of the batch
    i_end = min(len(data), i+batch_size)
    batch = data[i:i_end]

    # get ids from the batch
    ids_batch = batch['uid'].to_list()
    
    # get texts to encode
    texts = batch['chunk'].to_list()

    # create the embeddings to upload
    res = client.embeddings.create(
        input=texts,
        model=embed_model_id)
    resData = res.data
    embeds = [record.embedding for record in resData]

    # create metadata from the batch
    metadata = [{
        'chunk': x['chunk'],
        'source': x['source']
    } for _, x in batch.iterrows()]
    to_upsert = list(zip(ids_batch, embeds, metadata))
  
    # upsert to Pinecone database using index
    index.upsert(vectors=to_upsert)
  
