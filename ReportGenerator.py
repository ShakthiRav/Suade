from flask import Flask, render_template, request
from GetMetrics import *
app = Flask(__name__)
report = ""

@app.route('/',  methods=['GET'])
def hello():
    return render_template('dashboard.html', report = report)

@app.route('/',  methods=['POST'])
def update():
    date = request.form['date']
    report = getReport(date)

    return render_template('dashboard.html', report = report ,)

    
if __name__ == "__main__":
    app.run(debug = True)