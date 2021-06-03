from flask import render_template, url_for, flash, redirect, request, Blueprint
from .forms import registeroutForm, registerinForm
from ..models import *
from .. import db
from datetime import datetime
from ..utils import *

index = Blueprint("index", __name__)


@index.route("/")
@index.route("/home")
def home():
    vehicles = db.session.query(Vehicle).all()
    return render_template('menu.html', vehicles=vehicles, time_cheat=datetime.now().replace(microsecond=0).time())


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

        if not is_person_there(form.id_document.data):
            person = Person.query.filter_by(id_document=form.id_document.data).first_or_404()

            lot = Lot(is_available=False,
                      lot_type=form.vehicle_type.data)
            db.session.add(lot)
            db.session.commit()

            vehicle = None
            if not is_vehicle_there(form.license_plate.data):
                vehicle = Vehicle.query.filter_by(license_plate=form.license_plate.data).first_or_404()
            else:
                vehicle = Vehicle(license_plate=form.license_plate.data,
                                  vehicle_type=form.vehicle_type.data,
                                  owner_id_document=person.id_document,
                                  parking_lot_id=lot.id)
                db.session.add(vehicle)
                db.session.commit()

            usage = Usage(in_time=datetime.now(),
                          person_id_document=person.id_document)
            db.session.add(usage)
            db.session.commit()

            flash("El cliente ha reingresado satisfactoriamente.", 'primary')

            return redirect(url_for("index.home"))

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
                          owner_id_document=person.id_document,
                          parking_lot_id=lot.id)
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
        vehicle = Vehicle.query.filter_by(
            license_plate=form.license_plate.data).first_or_404()
        person = Person.query.filter_by(
            id_document=form.id_document.data).first_or_404()
        usage = Usage.query.filter_by(
            person_id_document=form.id_document.data).all()
        lot = Lot.query.filter_by(id=vehicle.parking_lot_id).first_or_404()

        usage[len(usage) - 1].out_time = datetime.now()
        usage[len(usage) - 1].total_charge = total_charge(vehicle.vehicle_type,
                                                          usage[len(usage) - 1].in_time, usage[len(usage) - 1].out_time)
        db.session.add(usage[len(usage) - 1])
        db.session.commit()

        db.session.delete(vehicle)
        db.session.commit()
        db.session.delete(lot)
        db.session.commit()

        flash(
            f"Eliminación exitosa, ahora la persona debe pagar un total de {usage[len(usage) - 1].total_charge}", "primary")
        return redirect(url_for("index.home"))

    return render_template('registerout.html', form=form,
                           car_occupied=car_occupied, bike_ocuppied=bike_ocuppied)


@index.route("/history/<id>")
def history(id):
    usages = Usage.query.filter_by(person_id_document=id).all()
    return render_template("usage_table.html", usages=usages)