from flask import Blueprint, render_template
from datetime import datetime

import sqlite3
import os

bp = Blueprint('main', __name__, url_prefix='/')
DB_FILE = os.environ.get("DB_FILE")

@bp.route('/')
def main():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime')
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        row[2] = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        row[3] = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')

    return render_template('main.html', rows=rows)
