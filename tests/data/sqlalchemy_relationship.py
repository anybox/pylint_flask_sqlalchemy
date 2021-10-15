"""Test sqlalchemy relationships."""
from .common import db


class Test(db.Model):
    """Test."""

    id = db.Column(db.Integer(), primary_key=True)
    subscriptions = db.relationship("Relation", lazy="dynamic")

    def lint_error(self):
        return self.subscriptions.filter(self.id < 0)


class Relation(db.Model):
    """Relation."""

    id = db.Column(db.Integer(), primary_key=True)
    list_id = db.Column(db.ForeignKey(Test.id, ondelete="CASCADE"), nullable=False)


# Used to raise a Instance of 'query' has no 'outerjoin' member (no-member)
# https://github.com/anybox/pylint_flask_sqlalchemy/issues/2
db.session.query(Test, Relation).outerjoin(Test, Relation.list_id == Test.id).all()
