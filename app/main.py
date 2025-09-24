from flask import Flask, request, send_file
from app.services import fetch_and_store_weather_data
from app.export_excel import generate_excel
from app.export_pdf import generate_pdf
app = Flask(__name__)


@app.route("/weather-report", methods=["GET"])
def weather_report():
    global lat, lon
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    fetch_and_store_weather_data(lat, lon)
    return {"message": "Weather data fetched and stored."}, 200


@app.route("/export/excel", methods=["GET"])
def export_excel():
    file_path = generate_excel()
    return send_file(file_path, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     as_attachment=True, download_name="weather_data.xlsx")


@app.route("/export/pdf", methods=["GET"])
def export_pdf():
    file_path = generate_pdf(lat,lon)
    return send_file(file_path, mimetype="application/pdf", as_attachment=True, download_name="weather_report.pdf")


if __name__ == "__main__":
    app.run(debug=True)
