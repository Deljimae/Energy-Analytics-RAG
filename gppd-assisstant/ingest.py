import pandas as pd
import minsearch

def load_index(data_path = '../data/data.csv'):
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