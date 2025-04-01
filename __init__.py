from flask import Flask, render_template, jsonify, request
from urllib.request import urlopen
from datetime import datetime
from collections import Counter
import json

app = Flask(__name__)

# Accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')

# Page de contact stylisée
@app.route("/contact/")
def contact():
    return render_template("contact.html")

# API météo Tawarano
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion K -> °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

# Page graphique de type ligne
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

# Histogramme Google Charts
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

# Outil de débogage : extraire les minutes d'une date ISO
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Graphique des commits (minuté)
@app.route("/commits/")
def commits():
    if request.headers.get("Accept") == "application/json":
        url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"  # Ton dépôt
        with urlopen(url) as response:
            commits_data = json.loads(response.read().decode("utf-8"))

        minutes = []
        for commit in commits_data:
            date_str = commit.get("commit", {}).get("author", {}).get("date")
            if date_str:
                dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                minutes.append(dt.minute)

        counts = Counter(minutes)
        return jsonify(results=[{"minute": k, "count": v} for k, v in sorted(counts.items())])

    return render_template("commits.html")

# Lancer l'app Flask
if __name__ == "__main__":
    app.run(debug=True)
