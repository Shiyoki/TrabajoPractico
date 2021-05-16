from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, ValidationError, SelectField
from wtforms.validators import DataRequired, Length
from ..models import Person


class registerinForm(FlaskForm):
    license_plate = StringField('Placa Vehicular: ', validators=[DataRequired("Este campo es obligatorio"),
                                                                 Length(min=1, max=7, message="La placa no debe estar vacia y no debe ser menor a 7 caracteres")])
    id_document = StringField('Cedula de Identidad: ', validators=[DataRequired("Este campo es obligatorio")])
    name = StringField('Nombre: ', validators=[DataRequired("Este campo es obligatorio")])
    vehicle_type = SelectField("Tipo de vehiculo", validators=[DataRequired(message="Este campo es obligatorio")], choices=['Seleccionar', 'C', 'M'])
    submit = SubmitField('Registrar')


class registeroutForm(FlaskForm):
    license_plate = StringField('Placa Vehicular: ')
    id_document = StringField('Cedula de Identidad: ')
    name = StringField('Nombre: ')
    submit = SubmitField('Verificar')