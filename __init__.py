from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

                                                                                                                                       
app = Flask(__name__) #5 
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route("/contact/")
def contact_form():
    return render_template("contact.html")

@app.route("/commits/")
def commits_graph():
    url = "https://api.github.com/repos/SdRfredyan/5MCSI_Metriques/commits"
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({"error": "Impossible de récupérer les commits"}), 500

    commits = response.json()
    minute_counts = Counter()

    for commit in commits:
        try:
            date_str = commit["commit"]["author"]["date"]  # Exemple : "2024-02-11T11:57:27Z"
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            minute = dt.minute
            minute_counts[minute] += 1
        except Exception as e:
            continue

    # On transforme les données en tableau [{minute: x, count: y}]
    data = [{"minute": m, "count": c} for m, c in sorted(minute_counts.items())]
    return render_template("commits.html", data=data)

  
if __name__ == "__main__":
  app.run(debug=True)
