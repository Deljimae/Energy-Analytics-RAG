# Energy-Analytics-RAG

## Problem Description

Accessing structured energy data is tedious and time-consuming. Analysts and researchers often need quick answers—such as “What’s the largest solar plant in the US?”—but must manually search large datasets like the Global Power Plant Database (GPPD).

This project builds a Retrieval-Augmented Generation APP that answers quantitative energy questions using the Global Power Plant Database (GPPD). The system ingests GPPD into a knowledge base (vector + text), retrieves relevant passages, builds prompts, queries an LLM, and evaluates performance on a ground-truth QA set generated from GPPD. This is the final project for the DTC's LLM Zoomcamp


## 🚀 Project Overview

**Energy-Analytics-RAG** is a lightweight Retrieval-Augmented Generation (RAG) application that enables users to explore and query power plant data from the **Global Power Plant Database (GPPD)** using natural language.  
Instead of manually filtering large CSV files, users can ask direct questions such as:  

- *“What is the largest solar plant in the United Kingdom?”*  
- *“When was the first hydro power plant in the U.S. commissioned?”*  
- *“List major gas plants commissioned after 2010.”*  

The system retrieves relevant entries from the knowledge base, constructs context-rich prompts, and uses an LLM to generate precise and verifiable answers.

## 📊 Dataset

This project uses the **Global Power Plant Database (GPPD)** — a comprehensive, open-source dataset compiled by the **World Resources Institute (WRI)**.  
It contains records of more than **34,000 power plants** across **190+ countries**, providing detailed information on each plant’s capacity, location, fuel type, ownership, and commissioning year.

For this project, a **subset of the dataset covering the United States and the United Kingdom** was used to keep the application lightweight and within free-tier limits.

### 🔑 Key Columns
- **country_long** – Full country name  
- **name** – Power plant name  
- **primary_fuel** – Main energy source (e.g., Solar, Hydro, Gas)  
- **capacity_mw** – Installed capacity in megawatts  
- **commissioning_year** – Year the plant began operation  
- **owner** – Organization that owns the plant  
- **latitude**, **longitude** – Geographic coordinates  

Additional columns such as **other_fuel1**, **generation_gwh_2021**, and **source** provide deeper context but were excluded in the lightweight subset to optimize retrieval performance.


### 🔍 Main Use Cases
- Energy research: Quickly obtain statistics and insights without complex queries.  
- Policy analysis: Retrieve information to support energy planning and sustainability goals.  
- Education: Help students and professionals learn about global power generation infrastructure.  
- LLM evaluation: Benchmark how well different LLMs handle quantitative reasoning over structured energy data.

## Technologies

* Minsearch for text search 
```bash
pip install minsearch
```
* LLM - Gemini 
* API interface - Flask (see [Technical Details](#technical-details) for more details)

## Getting Started

## Running it with Docker

Easiest way to run the application is to do so with docker

```bash
docker-compose up
```

If you need ro change something in the dockerfile and test it quickl, you can use the following commands:

```bash
docker build --no-cache -t energy-analytics-rag .

docker run -it --rm \
    -e GEMINI_API_KEY=${GEMINI_API_KEY} \
    -e DATA_PATH="data/data.csv" \
    -p 5000:5000 \
    energy-analytics-rag
```

### Preparing the Application

Before we can use the app, we need to initialize the database.

That can be done by running the [`db_prep.py`](gppd_assisstant/db_prep.py) script:
```bash

cd gppd_assisstant
export POSTGRES_HOST=localhost
python db_prep.py
```

The application will be available at http://127.0.0.1:5000

## Running Locally
### Environment Setup and Installation

If not using docker, installations should be done manually following below steps:

* 1. Create a .env file in the project root with your environment variables
* 2. Set up virtual env to run the code and Install the required dependencies 

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```


### Running the Application

Running the Flask application locally, do this:

```bash
source venv/bin/activate
export POSTGRES_HOST=localhost
python app.py
```

## Application Usage

Start the application eaither with docker compose or locally. You can then test it: 

Query Endpoint

Send a question about power plants:

```bash


URL=http://127.0.0.1:5000

QUESTION="What do you know about Drax power plant?"

DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
  -H "Content-Type: application/json" \
  -d "${DATA}" \
  ${URL}/question 

```

Example Response:

```json
{
  "answer": "There are two power plants named Drax mentioned in the context:\n\n1.  **Drax power plant**: Located in the United Kingdom, it is a Coal facility with a capacity of 1980 MW. It is located at latitude 54 and longitude -1.\n2.  **Drax GT power plant**: Also located in the United Kingdom, it is a Gas facility with a capacity of 75 MW. It is located at latitude 54 and longitude -1.",
  "conversation_id": "8bf6121b-7050-4b70-8dcf-100a943cfd58",
  "question": "What do you know about Drax power plant?"
}
```

Feedback Endpoint
Submit feedback for a conversation:

```bash
CONVERSATION_ID="8bf6121b-7050-4b70-8dcf-100a943cfd58"

FEEDBACK_DATA='{
    "conversation_id": "'${CONVERSATION_ID}'", 
    "feedback": 1
}'

curl -X POST \
  -H "Content-Type: application/json" \
  -d "${FEEDBACK_DATA}" \
  ${URL}/feedback 

```
Example Response:

```json
{
  "message": "Feedback received for conversation 8bf6121b-7050-4b70-8dcf-100a943cfd58 with feedback 1"
}
```

## Development 
Running Jupyter Notebook for experimentation:

```bash
cd notebooks    
jupyter notebook
```


## Interface

Flask was used for serving the application as an API.


## Evaluation

### Retrieval

Using minsearch without boosting give the following result;

* hit_rate: 98%
* mrr: 94%

The improved version(with better boosting):

* hit rate: 98%
* mrr: 96%

The best boosting parameters:

```python
boost = {
    'country_long': 0.28,
    'name':  0.90,
    'primary_fuel': 1.56,
    'capacity_mw': 0.72,
    'commissioning_year': 1.97,
    'passage': 1.28     
}
```

### Rag Flow

Planned Approach: LLM-as-a-Judge metric to evaluate responses as:

* X RELEVANT
* Y PARTIALLY RELEVANT
* Z IRRELEVANT  

Status: Due to resource constraints, automated RAG evaluation and model response benchmarking could not be completed at this time.


### Monitoring


### Ingestion

The ingestion script is implemented in  [gppd-assisstant/ingest.py](gppd-assisstant/ingest.py) and runs automatically when  [gppd-assisstant/rag.py](gppd-assisstant/rag.py) is executed.

## technical-details

### 🌐 Application Interface — Flask

The RAG application interface was built using **Flask**, a lightweight and flexible Python web framework. Flask handles the API layer of the project, allowing users to send queries to the retrieval-augmented generation (RAG) pipeline and receive model responses in real time.

It provides a simple route structure for interacting with the system and feedback collection.

For more details on Flask and its usage, visit the official documentation:  
👉 [https://flask.palletsprojects.com](https://flask.palletsprojects.com)


Note: Ensure you have a valid Google Gemini API key configured in your .env file before running the application.