from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ResearchForm(FlaskForm):
    jobName = StringField('jobName', validators=[DataRequired(), Length(min=2, max=70)])
    city = StringField('city', validators=[DataRequired(), Length(min=2, max=40)])
    companyName = StringField('companyName', validators=[DataRequired(), Length(min=2, max=40)])
    submit = SubmitField('Research')
