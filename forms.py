from flask_wtf import FlaskForm, CsrfProtect
from datetime import datetime, date
#from flask_wtf import Form
from wtforms import StringField, BooleanField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange, Regexp
from wtforms.fields import DateField
from wtforms_components import DateRange

class LoginForm(FlaskForm):
    iata = StringField('iata', validators=[InputRequired(), Regexp(r'[A-Z]'), Length(3,15,"Enter 3 Digit Airport Code")])
    region = SelectField(u'region', choices=[('east', 'East'), ('central', 'Central'), ('mountain', 'Mountain'), ('pacific', 'Pacific')])
    #minusd = IntegerField('minusd', validators=[InputRequired(), NumberRange(1,5000,"Enter Minimum of 1 USD")])
    #maxusd = IntegerField('maxusd', validators=[InputRequired(), NumberRange(1,5000,"Enter Maximum of 5,000 USD")])
    flyoutdate = DateField('flyoutdate', format='%m/%d/%Y', validators=[InputRequired(), DateRange(min=date.today())])
    #flyindate = DateField('flyindate', format='%m/%d/%Y', validators=[InputRequired(), DateRange(min=date.today())])
    #remember_me = BooleanField('remember_me', default=False)
