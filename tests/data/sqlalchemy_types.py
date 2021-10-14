"""Test sqlalchemy column."""
from .common import db


class Test(db.Model):
    """Test."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
