from flask import Flask, render_template, flash, redirect, sessions, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///pet_adoption"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config['SECRET_KEY'] = "abcdef"

connect_db(app)
db.create_all()

@app.route("/")
def home():
    """Home page with all pets listed. Includes their name, photo (if any) and availability"""
    pets = Pet.query.all()
    return render_template("index.html", pets = pets)

@app.route("/add", methods=["GET", "POST"])
def add():
    """GET and POST method to add a new pet"""
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name = name, species = species, photo_url = photo_url, age = age, notes = notes)

        db.session.add(pet)
        db.session.commit()
        flash(f"Added new pet")

        return redirect("/")
    else:
        return render_template("add_pet.html", form = form)

@app.route("/<pet_id>", methods=["GET", "POST"])
def edit(pet_id):
    """GET and POST method to edit the pet"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj = pet)

    if form.validate_on_submit():
        
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.add(pet)
        db.session.commit()
        flash(f"Updated pet")

        return redirect("/")
    else:
        return render_template("edit_pet.html", form = form, pet = pet)

@app.route("/<pet_id>/delete", methods=["POST"])
def remove(pet_id):
    """Delete pet from database"""

    pet = Pet.query.get_or_404(pet_id)

    db.session.delete(pet)
    db.session.commit()
    flash(f"Removed pet")

    return redirect("/")