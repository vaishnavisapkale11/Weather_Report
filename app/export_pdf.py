import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
import os
from weasyprint import HTML
import io, base64

DATABASE_URL = "sqlite:///weather.db"
engine = create_engine(DATABASE_URL, echo=False)

def generate_pdf(lat, lon):
    query = "SELECT timestamp, temperature, humidity FROM weather ORDER BY timestamp ASC"
    df = pd.read_sql(query, engine)
    if df.empty:
        raise ValueError("No weather data found. Call /weather-report first.")

    # Ensure timestamp is datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Date range metadata
    start_date = df["timestamp"].min().strftime("%Y-%m-%d %H:%M")
    end_date = df["timestamp"].max().strftime("%Y-%m-%d %H:%M")

    # ---------------- Chart ----------------
    plt.figure(figsize=(10, 5))

    ax1 = plt.gca()
    ax1.plot(df["timestamp"], df["temperature"], label="Temperature (°C)", color="red")
    ax1.set_ylabel("Temperature (°C)")
    ax1.legend(loc="upper left")

    ax2 = ax1.twinx()
    ax2.plot(df["timestamp"], df["humidity"], label="Humidity (%)", color="blue")
    ax2.set_ylabel("Humidity (%)")
    ax2.legend(loc="upper right")

    plt.title("Weather Report (Last 48 hours)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save chart as PNG → base64
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png")
    plt.close()
    img_bytes.seek(0)
    chart_b64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

    # ---------------- HTML ----------------
    html = f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ color: #333; }}
            .meta {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1>Weather Report</h1>
        <div class="meta">
            <p><b>Location:</b> Latitude {lat}, Longitude {lon}</p>
            <p><b>Date Range:</b> {start_date} → {end_date}</p>
        </div>
        <img src="data:image/png;base64,{chart_b64}" style="width:100%; max-width:700px;" />
    </body>
    </html>
    """

    file_path = "weather_report.pdf"
    HTML(string=html).write_pdf(file_path)
    return file_path

