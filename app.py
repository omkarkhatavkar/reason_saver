from flask import Flask, request, jsonify, render_template, redirect
import pusher
from database import db_session
from models import Failure
import os

app = Flask(__name__)

pusher_client = pusher.Pusher(
    app_id=os.getenv('PUSHER_APP_ID'),
    key=os.getenv('PUSHER_KEY'),
    secret=os.getenv('PUSHER_SECRET'),
    cluster=os.getenv('PUSHER_CLUSTER'),
    ssl=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    failures = Failure.query.all()
    return render_template('index.html', failures=failures)


@app.route('/backend', methods=["POST", "GET"])
def backend():
    if request.method == "POST":
        failure = request.form["failure"]
        count = request.form["count"]
        status = request.form["status"]

        new_failure = Failure(failure, count, status)
        db_session.add(new_failure)
        db_session.commit()

        data = {
            "id": new_failure.id,
            "failure": failure,
            "count": count,
            "status": status}
            
        pusher_client.trigger('my-channel', 'my-event', {'data': data})

        return redirect("/backend", code=302)
    else:
        failures = Failure.query.all()
        return render_template('backend.html', failures=failures)


@app.route('/edit/<int:id>', methods=["POST", "GET"])
def update_record(id):
    if request.method == "POST":
        failure = request.form["failure"]
        count = request.form["count"]
        status = request.form["status"]

        update_failure = Failure.query.get(id)
        update_failure.failure = failure
        update_failure.count = count
        update_failure.status = status

        db_session.commit()

        data = {
            "id": id,
            "failure": failure,
            "count": count,
            "status": status}

        pusher_client.trigger('my-channel', 'update-record', {'data': data })
       
        return redirect("/backend", code=302)
    else:
        new_failure = Failure.query.get(id)
        return render_template('update_failure.html', data=new_failure)


# run Flask app
if __name__ == "__main__":
    app.run()
