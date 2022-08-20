from flask import render_template, redirect, url_for, flash
from app import app
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import ContactForm, SignUpForm, LoginForm
from app.models import User, Contact

@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)


@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('A user with that username or email already exists.', 'danger') # BOOKMARK: format alerts
            return redirect(url_for('signup'))
        new_user = User(email=email,username=username,password=password)
        flash(f'User {new_user.username} has been created. Log in with your credentials.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)



@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'Login successful! Welcome back, {user.username}.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username or password incorrect. Please try again.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.','success')
    return redirect(url_for('index'))


@app.route('/new_contact', methods=['GET','POST'])
def new_contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        address = form.address.data
        notes = form.notes.data
        new_contact = Contact(name=name, phone=phone, address=address, notes=notes, user_id=current_user.id)
        flash(f'New contact {new_contact.name} has been created.','primary')
        return redirect(url_for('view_single_contact', contact_id=new_contact.contact_id))
    return render_template('new_contact.html', form=form)


@app.route('/contacts/<contact_id>')
@login_required
def view_single_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if contact.author != current_user:
        flash('You do not have permission to view this contact because you didn\'t create it.','warning')
        return redirect(url_for('index'))
    return render_template('view_contact.html', contact=contact)


@app.route('/contacts/<contact_id>/edit', methods=['GET','POST'])
@login_required
def edit_contact(contact_id):
    edit_contact = Contact.query.get_or_404(contact_id)
    if edit_contact.author != current_user:
        flash('You do not have permission to edit this contact because you didn\'t create it.','warning')
        return redirect(url_for('index'))
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        address = form.address.data
        notes = form.notes.data
        flash(f'Contact {name} successfully edited.','success')
        edit_contact.update(name=name, phone=phone, address=address, notes=notes)
        return redirect(url_for('view_single_contact', contact_id=edit_contact.contact_id))
    return render_template('edit_contact.html', contact=edit_contact, form=form)


@app.route('/contacts/<contact_id>/delete',methods=['GET','POST'])
@login_required
def delete_contact(contact_id):
    delete_contact = Contact.query.get_or_404(contact_id)
    if delete_contact.author != current_user:
        flash('You do not have permission to delete this contact because you didn\'t create it.', 'warning')
        return redirect(url_for('index'))
    delete_contact.delete()
    flash(f'{delete_contact.name} has been deleted.','success')
    return redirect(url_for('index'))