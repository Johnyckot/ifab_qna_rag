from elasticsearch import Elasticsearch
from openai import OpenAI
from sentence_transformers import SentenceTransformer

# define Elasticsearch client
es = Elasticsearch("http://elasticsearch:9200")
index_name = "idx_ifab_docs"

# define model for Embeddings calculation
model_name = 'all-mpnet-base-v2'
model = SentenceTransformer(model_name)

# # defing Openai client 
llm_client = OpenAI()


def retrieve_context(question, k = 5):
    """ 
    Retrieve context from Elasticsearch
    Returns a list of documents:url,topic_name,topic_text
    """

    vector_search_term = model.encode(question)
    
    query = {
        "field": "embedding",
        "query_vector": vector_search_term,
        "k": k,
        "num_candidates": 10000, 
    }
    
    res = es.search(index=index_name, knn=query, source=["h1", "h2", "h3", "text" , "url"])
    
    context_docs = []
    
    for r in res["hits"]["hits"]:
        headers = [ h.replace('\n',' ') for h in [ r['_source']['h1'], r['_source']['h2'], r['_source']['h3'] ]  ]
        topic_name = '. '.join(headers)
        context_docs.append(
            {'topic_name':topic_name,
             'url':r['_source']['url'],
             'topic_text':{r['_source']['text']}
            }
        )
    return(context_docs)

def create_prompt(question,context):
    """ 
    Builds a prompt from a question and a context.
    Returns a prompt string
    """
    context_string =  ''
    for c in context:
        context_string += f"""
        Source URL: {c['url']}
        Topic: {c['topic_name']}
        Topic content:
            {c['topic_text']}
        \n
        """
    prompt = f"""
    You are an expert in footbal rules. Answer the question using provided context. After the answer provide URL of the most relevant Context part.
    QUESTION: {question}
    
    CONTEXT{context_string}    
        
    """
    return prompt

def query_llm(prompt):    
    """ 
    Queries LLM with prompt.
    Returns an answer from LLM.
    """
    response = llm_client.chat.completions.create(
        model='gpt-4o',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


# question = "What's the difference between goal kick and free kick?"
# context = retrieve_context(question,1)
# prompt = create_prompt(question,context)
# answer = query_llm(prompt)


# print(answer)
