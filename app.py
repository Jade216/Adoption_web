from flask import Flask, render_template, redirect, flash, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
with app.app_context():
    db.create_all()

debug = DebugToolbarExtension(app)


@app.route('/')
def list_pets():
    '''homepage showing list of pets'''
    pets = Pet.query.all()
    return render_template('pet_list.html', pets = pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    '''add a pet'''
    form = AddPetForm()

    if form.validate_on_submit():
        data = {k:v for k,v in form.data.items() if k != 'csrf_token'}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f'{new_pet.name} added. ')
        return redirect(url_for('list_pets'))

    else:
        return render_template('pet_add_form.html', form = form)


@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    '''Edit pet'''
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f'{pet.name} updated. ')
        return redirect(url_for('list_pets'))
        
    else:
        return render_template('pet_edit_form.html', form = form, pet = pet)


@app.route('/api/pets/<int:pet_id>', methods=['GET'])
def api_get_pet(pet_id):
    '''return basic info of pet in JSON'''
    pet = Pet.query.get_or_404(pet_id)
    info = {'name': pet.name, 'species':pet.species, 'age':pet.age}

    return jsonify(info)