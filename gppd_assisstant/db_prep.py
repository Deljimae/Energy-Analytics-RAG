import pandas as pd
from tqdm.auto import tqdm
from dotenv import load_dotenv

from db import init_db


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
