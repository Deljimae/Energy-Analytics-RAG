# Energy-Analytics-RAG

## Problem Description

Accessing structured energy data is tedious and time-consuming. Analysts and researchers often need quick answers—such as “What’s the largest solar plant in the US?”—but must manually search large datasets like the Global Power Plant Database (GPPD).

This project builds a Retrieval-Augmented Generation APP that answers quantitative energy questions using the Global Power Plant Database (GPPD). The system ingests GPPD into a knowledge base (vector + text), retrieves relevant passages, builds prompts, queries an LLM, and evaluates performance on a ground-truth QA set generated from GPPD. This is the final project for the DTC's LLM Zoomcamp


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


## 🚀 Project Overview

**Energy-Analytics-RAG** is a lightweight Retrieval-Augmented Generation (RAG) application that enables users to explore and query power plant data from the **Global Power Plant Database (GPPD)** using natural language.  
Instead of manually filtering large CSV files, users can ask direct questions such as:  

- *“What is the largest solar plant in the United Kingdom?”*  
- *“When was the first hydro power plant in the U.S. commissioned?”*  
- *“List major gas plants commissioned after 2010.”*  

The system retrieves relevant entries from the knowledge base, constructs context-rich prompts, and uses an LLM to generate precise and verifiable answers.  

### 🔍 Main Use Cases
- **Energy research:** Quickly obtain statistics and insights without complex queries.  
- **Policy analysis:** Retrieve information to support energy planning and sustainability goals.  
- **Education:** Help students and professionals learn about global power generation infrastructure.  
- **LLM evaluation:** Benchmark how well different LLMs handle quantitative reasoning over structured energy data.


# Running It

Envirronmental variables were stored in a .env file


Set up virtual env to run code in (and install dependencies)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Running Jupyter Notebook for experiments after ensuring Jupyper notebook is installed:

```bash
cd notebooks    
jupyter notebook
```

