import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def get_weather_data(station, date):
    station_id = station.zfill(6)
    df = pd.read_csv(f"data_small/TG_STAID{station_id}.txt", skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == "1860-01-05"]['   TG'].squeeze() / 10
    return {'station': station, 'date': date, 'temperature': temperature}


if __name__ == "__main__":
    app.run(debug=True)
