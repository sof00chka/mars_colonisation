from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Работа', validators=[DataRequired()])
    team_leader = IntegerField('Руководитель')
    work_size = IntegerField('Объём работы')
    collaborators = StringField('Члены команды')
    start_date = DateTimeField('Дата начала', format='%Y-%m-%dT%H:%M')
    end_date = DateTimeField('Дата окончания', format='%Y-%m-%dT%H:%M')
    is_finished = BooleanField('Завершено')
    submit = SubmitField('Добавить')
