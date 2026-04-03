from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Coursework(db.Model):
    __tablename__ = 'coursework'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    course_unit = db.Column(db.String(100), nullable=False)
    marks_awarded = db.Column(db.Float, nullable=True)
    submission_deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Coursework {self.id}: {self.title}>'

    @property
    def deadline_formatted(self):
        return self.submission_deadline.strftime('%d %b %Y, %H:%M')

    @property
    def deadline_input_value(self):
        """Format for datetime-local HTML input."""
        return self.submission_deadline.strftime('%Y-%m-%dT%H:%M')

    @property
    def is_overdue(self):
        return self.submission_deadline < datetime.utcnow() and self.status == 'pending'
