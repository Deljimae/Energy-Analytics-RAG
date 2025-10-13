import pandas as pd
import minsearch
import os 

DATA_PATH = os.getenv('DATA_PATH', '../data/data.csv')

def load_index(data_path = DATA_PATH):
    df = pd.read_csv(data_path)

    documents = df.to_dict(orient='records')

    index = minsearch.Index(
        text_fields=[
            'country_long',
            'name',
            'passage'
        ],
        keyword_fields=['id']
    )

    index.fit(documents)
    return index