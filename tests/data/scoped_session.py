from tests.data.common import db, User

user = User(username="test")
db.session.add(user)
db.session.commit()
