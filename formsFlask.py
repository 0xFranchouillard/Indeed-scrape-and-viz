from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ResearchForm(FlaskForm):
    jobName = StringField('jobName')
    city = StringField('city')
    companyName = StringField('companyName')
    submit = SubmitField('Research')
