import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)
stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[['STAID', 'STANAME                                 ']]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def get_weather_data(station, date):
    station_id = station.zfill(6)
    df = pd.read_csv(f"data_small/TG_STAID{station_id}.txt", skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == "1860-01-05"]['   TG'].squeeze() / 10
    return {'station': station, 'date': date, 'temperature': temperature}


@app.route("/api/v1/<station>")
def all_data_for_one_station(station):
    station_id = station.zfill(6)
    df = pd.read_csv(f"data_small/TG_STAID{station_id}.txt", skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/year/<station>/<year>")
def yearly_data_for_one_station(station, year):
    station_id = station.zfill(6)
    df = pd.read_csv(f"data_small/TG_STAID{station_id}.txt", skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True)
