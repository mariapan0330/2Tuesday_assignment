from flask import render_template
from app import app
from app.forms import ContactForm
from app.models import Contact

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_contact', methods=['GET','POST'])
def new_contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        address = form.address.data
        notes = form.notes.data
        new_contact = Contact(name=name, phone=phone, address=address, notes=notes)
    return render_template('new_contact.html', form=form)


# @app.route('/show_contacts')
# def show_contacts():
#     return render_template('show_contacts.html')