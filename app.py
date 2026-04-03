from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Coursework
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coursework.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'course-buddy-secret-key-2024'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    entries = Coursework.query.order_by(Coursework.submission_deadline.asc()).all()
    total = len(entries)
    pending = sum(1 for e in entries if e.status == 'pending')
    submitted = sum(1 for e in entries if e.status == 'submitted')
    graded = sum(1 for e in entries if e.status == 'graded')
    return render_template(
        'index.html',
        entries=entries,
        total=total,
        pending=pending,
        submitted=submitted,
        graded=graded
    )


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        course_unit = request.form.get('course_unit', '').strip()
        marks_raw = request.form.get('marks_awarded', '').strip()
        deadline_raw = request.form.get('submission_deadline', '').strip()
        status = request.form.get('status', 'pending')

        errors = []
        if not title:
            errors.append('Title is required.')
        if not course_unit:
            errors.append('Course unit is required.')
        if not deadline_raw:
            errors.append('Submission deadline is required.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('form.html', mode='add', coursework=None, form_data=request.form)

        try:
            deadline = datetime.strptime(deadline_raw, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid deadline format.', 'error')
            return render_template('form.html', mode='add', coursework=None, form_data=request.form)

        marks = None
        if marks_raw:
            try:
                marks = float(marks_raw)
            except ValueError:
                flash('Marks must be a valid number.', 'error')
                return render_template('form.html', mode='add', coursework=None, form_data=request.form)

        entry = Coursework(
            title=title,
            course_unit=course_unit,
            marks_awarded=marks,
            submission_deadline=deadline,
            status=status
        )
        db.session.add(entry)
        db.session.commit()
        flash(f'"{title}" added successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', mode='add', coursework=None, form_data={})


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    entry = Coursework.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        course_unit = request.form.get('course_unit', '').strip()
        marks_raw = request.form.get('marks_awarded', '').strip()
        deadline_raw = request.form.get('submission_deadline', '').strip()
        status = request.form.get('status', 'pending')

        errors = []
        if not title:
            errors.append('Title is required.')
        if not course_unit:
            errors.append('Course unit is required.')
        if not deadline_raw:
            errors.append('Submission deadline is required.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('form.html', mode='edit', coursework=entry, form_data=request.form)

        try:
            deadline = datetime.strptime(deadline_raw, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid deadline format.', 'error')
            return render_template('form.html', mode='edit', coursework=entry, form_data=request.form)

        marks = None
        if marks_raw:
            try:
                marks = float(marks_raw)
            except ValueError:
                flash('Marks must be a valid number.', 'error')
                return render_template('form.html', mode='edit', coursework=entry, form_data=request.form)

        entry.title = title
        entry.course_unit = course_unit
        entry.marks_awarded = marks
        entry.submission_deadline = deadline
        entry.status = status
        db.session.commit()
        flash(f'"{title}" updated successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', mode='edit', coursework=entry, form_data={})


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    entry = Coursework.query.get_or_404(id)
    title = entry.title
    db.session.delete(entry)
    db.session.commit()
    flash(f'"{title}" deleted.', 'success')
    return redirect(url_for('index'))


@app.route('/update-status/<int:id>', methods=['POST'])
def update_status(id):
    entry = Coursework.query.get_or_404(id)
    data = request.get_json()
    new_status = data.get('status') if data else None
    valid_statuses = ['pending', 'submitted', 'graded']
    if new_status not in valid_statuses:
        return jsonify({'success': False, 'error': 'Invalid status'}), 400
    entry.status = new_status
    db.session.commit()
    return jsonify({'success': True, 'status': entry.status})


if __name__ == '__main__':
    app.run(debug=True)
