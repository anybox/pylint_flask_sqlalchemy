"""Test sqlalchemy column."""
from .common import db


class Test(db.Model):
    """Test."""
    id = db.Column(db.Integer, primary_key=True)
