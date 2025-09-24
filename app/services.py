import pandas
import requests
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///weather.db"

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String, unique=True, nullable=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


def save_df_to_db(df: pd.DataFrame):
    """
    Save weather data from a DataFrame into the SQLite DB.
    Expects columns: ['timestamp', 'temperature', 'humidity']
    """
    session = SessionLocal()
    try:
        for _, row in df.iterrows():

            exists = session.query(WeatherData).filter_by(timestamp=str(row["timestamps"])).first()
            print(exists)
            if not exists:
                record = WeatherData(
                    timestamp=str(row["timestamps"]),
                    temperature=row["temperature"],
                    humidity=row["humidity"],
                )
                session.add(record)
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

def fetch_and_store_weather_data(lat, lon):
    end = datetime.now()
    start = end - timedelta(days=2)
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start.date()}&end_date={end.date()}"
        f"&hourly=temperature_2m,relative_humidity_2m&timezone=UTC"
    )

    response = requests.get(url)
    data = response.json()


    timestamps = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    humidity = data["hourly"]["relative_humidity_2m"]
    df=pandas.DataFrame({'timestamps':timestamps, 'temperature':temps,'humidity':humidity})
    save_df_to_db(df.astype(str))
