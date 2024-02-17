from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, TimeField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime

class AppointmentForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    start_date = DateField('start_date', validators=[DataRequired()])
    start_time = TimeField('start_time', validators=[DataRequired()])
    end_date = DateField('end_date', validators=[DataRequired()])
    end_time = TimeField('end_time', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    private = BooleanField('private')
    submit = SubmitField('Create Appointment')

    def validate_end_date(form, field):
        start = datetime.combine(form.start_date.data, form.start_time.data)
        end = datetime.combine(field.data, form.end_time.data)

        if start >= end:
            msg = "End date/time must come after start date/time"
            raise ValidationError(msg)

        if form.start_date.data != form.end_date.data:
            raise ValidationError('Start date and End date must be on the same date')
