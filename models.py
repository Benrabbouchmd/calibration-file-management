from db import db
from time import time


class CalibrationFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pandora_id = db.Column(db.String)
    spectrometer_id = db.Column(db.String)
    version = db.Column(db.String)
    validity_date = db.Column(db.String)
    content = db.Column(db.Text)
    created_at = db.Column(db.Integer, default=lambda: int(time()))
    updated_at = db.Column(
        db.Integer, default=lambda: int(time()), onupdate=lambda: int(time())
    )
    file_hash = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return f"CalibrationFile('{self.pandora_id}', '{self.spectrometer_id}', '{self.version}', '{self.validity_date}')"
