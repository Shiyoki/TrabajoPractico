from . import db
from .models import *
from datetime import datetime

def occupied_lot(lot_type):
    return len([lot for lot in Lot.query.filter_by(lot_type=lot_type) if not lot.is_available])


def is_full(lot_type):
    return len([lot for lot in Lot.query.filter_by(lot_type=lot_type) if not lot.is_available]) >= 24 if lot_type == "C" else len([lot for lot in Lot.query.filter_by(lot_type=lot_type) if not lot.is_available]) >= 6


def total_charge(type, vehicle_plate, ):
    if type == "C":
        pass


