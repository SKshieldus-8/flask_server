from flask.cli import FlaskGroup

from project.main import app, db


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# @cli.command("seed_db")
# def seed_db():
    # db.session.add(User(name="BillyMin", password="1234!"))
    # db.session.commit()


if __name__ == "__main__":
    cli()