from flask import render_template
from app import app
from app.forms import AddresseeForm
from app.models import Addressee

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_address', methods=['GET','POST'])
def new_address():
    form = AddresseeForm()
    if form.validate_on_submit():
        print('Addressee successfully validated')
        name = form.name.data
        phone = form.phone.data
        address = form.address.data
        new_addressee = Addressee(name=name, phone=phone, address=address)
    return render_template('new_address.html', form=form)


@app.route('/show_addresses')
def show_addresses():
    return render_template('show_addresses.html')