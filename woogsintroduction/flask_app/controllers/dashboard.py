from flask_app import app
from flask import render_template, request, flash, redirect, session
from flask_app.models.user import User
from flask_app.models.sasq import Sasq

@app.route('/dashboard')
def list():

    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")
    user = User.get_user_by_id(session["uid"])
    sasqs = Sasq.get_all()
    return render_template("dashboard.html", user=user, sasqs=sasqs)

@app.route('/report')
def report():
    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")
    user = User.get_user_by_id(session["uid"])
    return render_template('report.html', user=user)

@app.route('/report', methods=['POST'])
def report_post():
    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")
    is_valid, errors = Sasq.validate(request.form)
    if not is_valid:
        for error in errors:
            flash(error, "error")
        user = User.get_user_by_id(session["uid"])
        return render_template("report.html", user=user)
    print(request.form["location"])
    print(request.form["whathappened"])
    print(request.form["numberof"])
    Sasq.save({
        "location": request.form["location"],
        "whathappened": request.form["whathappened"],
        "numberof": request.form["numberof"],
        "made_at": request.form["made_at"],
        "user_id": session["uid"]
    })

    return redirect('/report')


@app.route('/report/<report_id>')
def view_report(report_id):
    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")
    user = User.get_user_by_id(session["uid"])
    report = Sasq.get_sasq_by_id(report_id)
    return render_template("view.html", user=user, report=report)


@app.route('/report/<report_id>/edit')
def edit_report(report_id):
    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")
    user = User.get_user_by_id(session["uid"])
    report = Sasq.get_sasq_by_id(report_id)
    return render_template("edit.html", user=user, report=report)

@app.route('/report/<report_id>/edit', methods=['post'])
def edit_report_post(report_id):
    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")
    user = User.get_user_by_id(session["uid"])
    is_valid, errors = Sasq.validate(request.form)
    if not is_valid:
        for error in errors:
            flash(error, "error")
        user = User.get_user_by_id(session["uid"])
        return redirect("/report/" + report_id + "/edit")
    report = Sasq.get_sasq_by_id(report_id)
    if report.user_id != user.id:
        flash("Insufficient permissions to edit report.")
        return redirect("/dashboard")

    Sasq.edit_sasq({
        "id": report_id,
        "location": request.form["location"],
        "whathappened": request.form["whathappened"],
        "numberof": request.form["numberof"],
        "made_at": request.form["made_at"],
    })
    return render_template("edit.html", user=user, report=report)


@app.route('/report/<report_id>/delete', methods=['get', 'post'])
def delete_report(report_id):
    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")

    report = Sasq.get_sasq_by_id(report_id)
    if report.user_id != session["uid"]:
        flash("Insufficient permissions to delete report.")
        return redirect("/dashboard")

    Sasq.delete_sasq_by_id(report_id)
    return redirect("/dashboard")
