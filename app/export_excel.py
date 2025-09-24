import pandas as pd
from sqlalchemy import create_engine
import os

DATABASE_URL = "sqlite:///weather.db"
engine = create_engine(DATABASE_URL, echo=False)

def generate_excel(file_path: str = "weather_data.xlsx"):
    # Read all records from the table
    query = "SELECT timestamp, temperature, humidity FROM weather ORDER BY timestamp ASC"
    df = pd.read_sql(query, engine)

    if df.empty:
        raise ValueError(" No data found in database. Please run service.py first to fetch data.")

    # Save DataFrame to Excel
    df.to_excel(file_path, index=False)

    return os.path.abspath(file_path)

