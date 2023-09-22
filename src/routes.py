from flask import render_template, request, redirect, url_for, make_response, session
from src import app, db
from src.utils import generate_report
import json, csv
from io import StringIO

@app.get("/")
def landing_page():
    with app.app_context():
        db.create_all()
    return render_template("main.html")

@app.post("/trigger_report")
def trigger_report():
    global report
    storeID = request.form["storeID"]
    report = generate_report(storeID)
    return redirect(url_for("get_report", report = json.dumps(report)))

@app.route("/get_report")
def get_report():
    report = json.loads(request.args.get('report'))
    session["report"] = json.dumps(report)
    return render_template("download.html", filename = f'{report[1][0]}.csv', report = report)

@app.get("/download_report")
def download_report():
    report = json.loads(session.get("report"))
    session.pop("report")
    output = StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerows(report)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename={report[1][0]}.csv'
    return response