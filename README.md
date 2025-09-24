# Weather Report Service (Flask + SQLite + Docker)

This project is a simple backend service built with **Flask** that:
- Fetches **time-series weather data** (temperature & humidity) from the [Open-Meteo API](https://open-meteo.com).
- Stores the data in a **SQLite database**.
- Exports the stored data as:
  - An **Excel file** (`.xlsx`).
  - A **PDF report** with a line chart of temperature & humidity vs time.


## ⚙️ Installation & Setup

### 1️⃣ Clone this repository
```bash
git clone <your-repo-url>
cd project
```

### 1️⃣ Create a virtual environment and Install Dependencies
```bash
 python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
```

### 1️⃣ Run Flask app
```bash
python app/main.py
```

### 🐳 Run with Docker(optional)
```bash
docker build -t weather-service .
```

### 🐳 Run container
```bash
docker run -p 5000:5000 weather-service
```
### 🌐 API Endpoints
#### 1️⃣ Fetch & Store Weather Data
Fetches weather data for the last 2 days for a given location using following url.
you have to pass latitude and longitude in url so you can get weather data for this particular location

```bash
http://127.0.0.1:5000/weather-report?lat={lattitude}&lon={longitude}
```

#### 2️⃣ Export Data to Excel
Exports the last 48 hours of data from the SQLite DB into an .xlsx file.
```bash
http://127.0.0.1:5000/export/excel
```
#### 23️⃣ Export Data to PDF
##### Generates a PDF report with:

Title & metadata (location, date range).

A line chart (temperature & humidity vs time).
```bash
http://127.0.0.1:5000/export/pdf
```
This will download a file named weather_report.pdf
