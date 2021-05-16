from . import db
from .models import *
from datetime import datetime


def occupied_lot(lot_type):
    return len([lot for lot in Lot.query.filter_by(lot_type=lot_type) if not lot.is_available])


def is_full(lot_type):
    return len([lot for lot in Lot.query.filter_by(lot_type=lot_type) if not lot.is_available]) >= 24 if lot_type == "C" else len([lot for lot in Lot.query.filter_by(lot_type=lot_type) if not lot.is_available]) >= 6


def total_charge(vehi_type, person_id_document):
    initial_charge = {"C": 0.50,
                      "M": 0.40}
    fee_per_hour = {"C": 0.40,
                    "M": 0.30}

    recent_usage = Usage.query.filter_by(
        person_id_document=perso_id_document).all()
    hours = recent_usage[len(recent_usage) - 1].out_time - \
        recent_usage[len(recent_usage) - 1].in_time

    return (initial_charge[vehi_type] * (int(round(hours.seconds / 3600)) * fee_per_hour[vehi_type]))




