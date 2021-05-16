from flask import render_template, url_for, flash, redirect, request, Blueprint
from .forms import registeroutForm, registerinForm
from ..models import *
from .. import db
from datetime import datetime
from ..utils import occupied_lot, is_full

index = Blueprint("index", __name__)


@index.route("/")
@index.route("/home")
def home():
    return render_template('menu.html')


@index.route("/registerin", methods=["GET", "POST"])
def registerin():
    form = registerinForm()
    car_occupied = occupied_lot("C")
    bike_ocuppied = occupied_lot("M")

    if form.validate_on_submit():
        if is_full(form.vehicle_type.data):
            if form.vehicle_type.data == "C":
                flash("Ya no quedan puestos disponibles para vehiculos", "primary")
            else:
                flash("Ya no quedan puestos disponibles para motos", "primary")

            return redirect(url_for("index.registerin"))

        person = Person(name=form.name.data,
                        id_document=form.id_document.data)
        db.session.add(person)
        db.session.commit()

        lot = Lot(is_available=False,
                  lot_type=form.vehicle_type.data)
        db.session.add(lot)
        db.session.commit()

        vehicle = Vehicle(license_plate=form.license_plate.data,
                          vehicle_type=form.vehicle_type.data,
                          owner_id=person.id,
                          parking_lot_id=lot.id
                          )
        db.session.add(vehicle)
        db.session.commit()

        usage = Usage(in_time=datetime.now(),
                      person_id_document=person.id_document)
        db.session.add(usage)
        db.session.commit()

        flash("El cliente se registro satisfactoriamente.", 'primary')

        return redirect(url_for("index.home"))

    return render_template('registerin.html', form=form,
                           car_occupied=car_occupied, bike_ocuppied=bike_ocuppied)


@index.route("/registerout", methods=["GET", "POST"])
def registerout():
    form = registeroutForm()
    car_occupied = occupied_lot("C")
    bike_ocuppied = occupied_lot("M")

    if form.validate_on_submit():
        pass

    return render_template('registerout.html', form=form,
                           car_occupied=car_occupied, bike_ocuppied=bike_ocuppied)