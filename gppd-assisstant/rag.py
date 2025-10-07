import ingest
import os
from google import genai
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

index = ingest.load_index()


def search(query):    
    results = index.search(
        query=query,
        filter_dict={},
        num_results=10
    )
    return results


prompt_template = """
You're an Energy plants assistant. Answer the QUESTION based on the CONTEXT from the GPPD.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT: 
{context}
""".strip()


entry_template = """
country_long: {country_long},
name: {name},
primary_fuel: {primary_fuel},
capacity_mw: {capacity_mw},
commissioning_year: {commissioning_year},
passage: {passage}
""".strip()
    
def build_prompt(query, search_results):
    context = ""
    
    for doc in search_results:
        context = context + entry_template.format(**doc) + "\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def llm(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def rag(query):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer
