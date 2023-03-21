from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/staff', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            # providing the schema for the note
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)  # adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("staff.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # this function expects a JSON from the INDEX.js file
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/budget_summary', methods=['GET', 'POST'])
def budget_summary():
    if request.method == 'POST':
        budget = int(request.form['budget'])
        transportation = int(request.form['transportation'])
        accommodation = int(request.form['accommodation'])
        food = int(request.form['food'])
        activities = int(request.form['activities'])
        total = transportation + accommodation + food + activities
        remaining = budget - total
        return render_template('budget_summary.html', total=total, remaining=remaining)


@views.route('/budget_planner')
def budget_planner():
    return render_template('budget_planner.html')


@views.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


@views.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    print(name,email,message)
    return 'Thank you for your message!'

@views.route('/places_to_visit')
def places_to_visit():
    return render_template('places_to_visit.html')


@views.route('/homestay_tourism')
def homestay_tourism():
    return render_template('homestay_tourism.html')
