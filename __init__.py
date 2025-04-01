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

  
if __name__ == "__main__":
  app.run(debug=True)
