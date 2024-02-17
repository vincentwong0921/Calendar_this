from flask import Blueprint, render_template, redirect, url_for
from datetime import datetime, timedelta
from app.forms import AppointmentForm

import sqlite3
import os

bp = Blueprint('main', __name__, url_prefix='/')
DB_FILE = os.environ.get("DB_FILE")

@bp.route('/', methods=['GET', 'POST'])
def main():
    today = datetime.now()
    return redirect(url_for(".daily", year=today.year, month=today.month, day=today.day))

@bp.route('/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
def daily(year, month, day):
    form = AppointmentForm()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    day = datetime(year, month, day)
    next_day = day + timedelta(days = 1)
    if form.validate_on_submit():
        params = {
            'name': form.name.data,
            'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
            'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
            'description': form.description.data,
            'private': form.private.data
        }
        cursor.execute('''INSERT INTO appointments (name, start_datetime, end_datetime, description, private) VALUES (?, ?, ?, ?, ?);''',
                       (params["name"], params["start_datetime"], params["end_datetime"], params["description"], params["private"]))
        conn.commit()
        conn.close()
        return redirect('/')

    cursor.execute('SELECT id, name, start_datetime, end_datetime FROM appointments WHERE start_datetime BETWEEN ? AND ? ORDER BY start_datetime;', (day, next_day))
    rows = cursor.fetchall()
    conn.close()
    appointments = []

    for row in rows:
        appointments.append((row[0], row[1], datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S').strftime("%H:%M"), datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S').strftime("%H:%M")))
    return render_template('main.html', rows=appointments, form=form)


##  rows = [(1, 'My appointment', '2024-02-15 14:00:00', '2024-02-15 15:00:00')]
