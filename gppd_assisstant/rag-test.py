

import pandas as pd
import os
from tqdm.auto import tqdm


# In[2]:




# In[13]:


question = 'What is the commissioning year for the 14 Tullywiggan Road power plant?'
answer = rag(question)
print(answer)


# In[ ]:





# ## Retrieval Evaluation

# In[14]:


df_question = pd.read_csv('../data/ground-truth-retrieval.csv')


# In[15]:


df_question.head()


# In[16]:


df_question = pd.read_csv('../data/ground-truth-retrieval.csv')

ground_truth = df_question.to_dict(orient='records')

def hit_rate(relevance_total):
    cnt = 0

    for line in relevance_total:
        if True in line:
            cnt = cnt + 1

    return cnt / len(relevance_total)
def mrr(relevance_total):
    total_score = 0.0

    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank] == True:
                total_score = total_score + 1 / (rank + 1)

    return total_score / len(relevance_total)

def minsearch_search(query):
    results = index.search(
        query=query,
        filter_dict={},
        num_results=10
    )
    return results


def evaluate(ground_truth, search_function):
    relevance_total = []

    for q in tqdm(ground_truth):
        doc_id = q['id']
        results = search_function(q)
        relevance = [d['id'] == doc_id for d in results]
        relevance_total.append(relevance)

    return {
        'hit_rate': hit_rate(relevance_total),
        'mrr': mrr(relevance_total),
    }

evaluate(ground_truth, lambda q: minsearch_search(q['question']))


# In[18]:


ground_truth = df_question.to_dict(orient='records')


# In[19]:


ground_truth[0]


# In[ ]:





# In[20]:


def hit_rate(relevance_total):
    cnt = 0

    for line in relevance_total:
        if True in line:
            cnt = cnt + 1

    return cnt / len(relevance_total)
def mrr(relevance_total):
    total_score = 0.0

    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank] == True:
                total_score = total_score + 1 / (rank + 1)

    return total_score / len(relevance_total)


# In[ ]:





# In[21]:


def minsearch_search(query):
    results = index.search(
        query=query,
        filter_dict={},
        num_results=10
    )
    return results


# In[22]:


def evaluate(ground_truth, search_function):
    relevance_total = []

    for q in tqdm(ground_truth):
        doc_id = q['id']
        results = search_function(q)
        relevance = [d['id'] == doc_id for d in results]
        relevance_total.append(relevance)

    return {
        'hit_rate': hit_rate(relevance_total),
        'mrr': mrr(relevance_total),
    }


# In[23]:


from tqdm.auto import tqdm


# In[24]:


evaluate(ground_truth, lambda q: minsearch_search(q['question']))


# In[ ]:





# ## Finding the best Parameter

# In[25]:


df_validation = df_question[:100]
df_test = df_question[100:]


# In[26]:


import random

def simple_optimize(param_ranges, objective_function, n_iterations=10):
    best_params = None
    best_score = float('-inf') # for maximizing 

    for _ in range(n_iterations):
        # generate random parameters
        current_params = {}
        for param, (min_val, max_val) in param_ranges.items():
            if isinstance(min_val, int) and isinstance(max_val, int):
                current_params[param] = random.randint(min_val, max_val)
            else:
                current_params[param] = random.uniform(min_val, max_val)

        # evaluate the objecctive function
        current_score = objective_function(current_params)

        # Update best if current is better
        if current_score > best_score:
            best_score = current_score
            best_param =current_params

    return best_param, best_score

# Example_usage: 
def example_objective(x, y):
    return (x - 3)**2 + (y - 2)**2

param_ranges = {
    'x': (-10, 10),
    'y': (-10, 10),
}
            


# In[27]:


best_params, best_score = simple_optimize(param_ranges, objective, n_iterations=10)
print(f"Best parameters: {best_params}")
print(f"Best score: {best_score}")


# In[28]:


gt_val = df_validation.to_dict(orient='records')


# In[29]:


def minsearch_search(query, boost=None):
    if boost is None:
        boost = {}
        
    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )
    return results


# In[ ]:





# In[30]:


param_ranges = {
    'country_long': (0.0,3.0),
    'name': (0.0,3.0),
    'primary_fuel': (0.0,3.0),
    'capacity_mw': (0.0,3.0),
    'commissioning_year': (0.0,3.0),
    'passage': (0.0,3.0),
}

def objective(boost_params):
    def search_function(q):
        return minsearch_search(q['question'], boost_params)

    results = evaluate(gt_val, search_function)
    return results['mrr']


# In[116]:


simple_optimize(param_ranges, objective, n_iterations=10)


# In[31]:


def minsearch_improved(query):
    boost = {
        'country_long': 0.28,
        'name':  0.90,
        'primary_fuel': 1.56,
        'capacity_mw': 0.72,
        'commissioning_year': 1.97,
        'passage': 1.28     
    }
          
    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )
    return results


# In[32]:


evaluate(ground_truth, lambda q: minsearch_improved(q['question']))


# In[ ]:





# ## RAG Evaluation

# In[33]:


prompt2_template = """
You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer_llm}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()


# In[34]:


len(ground_truth)


# In[35]:


record = ground_truth[0]


# In[36]:


question = record['question']


# In[37]:


answer_llm = rag(question)


# In[38]:


print(answer_llm)


# In[39]:


prompt = prompt2_template.format(answer_llm=answer_llm, question=question)
print(prompt)


# In[40]:


print(llm(prompt))


# In[52]:


import json


# In[53]:


df_sample = df_question.sample(n=200, random_state=1)


# In[54]:


sample = df_sample.to_dict(orient='records')


# In[55]:


evaluations = {}


# In[57]:


import json

evaluations = []

for record in tqdm(ground_truth[:5]):
    question = record['question']
    answer_llm = rag(question)

    prompt = prompt2_template.format(
        question=question,
        answer_llm=answer_llm
    )
    evaluation = llm(prompt)
    evaluation: json.loads(evaluation)

    evaluations.append((record, answer_llm, evaluation))


# In[50]:


df_eval = pd.DataFrame(evaluations).T


# In[51]:


df_eval.head()


# In[ ]:




