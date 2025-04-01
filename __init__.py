from flask import Flask, render_template, jsonify, request
from urllib.request import urlopen
from datetime import datetime
from collections import Counter
import json

                                                                                                                                       
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
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    try:
        req = urlopen(
            urllib.request.Request(
                url,
                headers={"Authorization": "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"}
            )
        )
        raw_data = req.read()
        commits = json.loads(raw_data.decode("utf-8"))
    except Exception as e:
        return jsonify({"error": "Erreur lors de la récupération des commits", "details": str(e)}), 500

    minute_counts = Counter()

    for commit in commits:
        try:
            date_str = commit["commit"]["author"]["date"]
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            minute = dt.minute
            minute_counts[minute] += 1
        except Exception:
            continue

    data = [{"minute": m, "count": c} for m, c in sorted(minute_counts.items())]
    return render_template("commits.html", data=data)

  
if __name__ == "__main__":
  app.run(debug=True)
