# libraries we need to use

# import sqlite3
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# from werkzeug.utils import secure_filename

from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, session,  Response, Request
from .models import students, admin, poll,  vice as can2, president as can
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import *


app = Flask(__name__)
auth = Blueprint('auth', __name__)


# home page route
@auth.route('/home', methods=['GET', 'POST'])
def home():

    return redirect(url_for("views.home"))


@auth.route('/adminLogin', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        adminUsername = request.form.get('adminUsername')
        adminPassword = request.form.get('adminPassword')

        user = admin.query.filter_by(adminUsername=adminUsername).first()
        if user:

            if check_password_hash(user.adminPassword, adminPassword):
                login_user(user, remember=True)
                flash("admin logged in successfully!", category='success')
                # print("admin:",adminUsername, "password:", adminPassword)
                redirect(url_for("auth.admin_maintain"))
#                return render_template("admin_maintain.html", user=current_user)
            else:
                flash("incorrect password, try again.", category='error')
        else:
            flash("admin Username does not exist.", category='error')

    return render_template("adminLogin.html", user=current_user)


# sign up page route
@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():

   if request.method == 'POST':

        firstName = request.form['exampleInputFirstname']
        lastName = request.form['exampleInputLastname']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if len(firstName) < 2:
           flash("first name must be greater than 2", category='error')
        elif len(lastName) < 2:
           flash("last name must be greater than 2", category='error')
        elif len(email) < 4:
           flash("Email must be greater than 4", category='error')
        elif password1 != password2:
            flash("passwords do not match", category='error')
        elif len(password1) < 7:
            flash("password must be greater than 7", category='error')
        elif students.query.filter_by(email=email).first():
            flash("email already exists!", category='error')
        else:
            flash("account created,  you can proceed to log in", category='success')
            new_user = students(firstName=firstName, lastName=lastName, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for('auth.sign_up'))

   return render_template("sign_up.html", user=current_user)


# login page route
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        user = students.query.filter_by(email=email).first()

        if user:

            if check_password_hash(user.password, password):

                flash("logged in successfully!", category='success')
                login_user(user, remember=True)

                # print("this is the current user's password:", current_user.password)
                # return render_template("categories.html", user=current_user)
            else:
                flash("incorrect password, try again.", category='error')

        else:
            flash("Email does not exist.", category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():

    logout_user()

    #    after_request()
    flash("Logged out successfully", category='success')
    return redirect(url_for('auth.login'))


@auth.route('/admin_maintain', methods=['GET', 'POST'])
@login_required
# @login_user(user=current_user)
def admin_maintain():

    if request.method == 'POST':

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        manifesto = request.form['manifesto']
        post = request.form.getlist('options')

# to convert the list to string
        str_choice = '' .join(post)

        if str_choice == 'president':
            if can.query.filter_by(email=email).first():
                flash("email already exists!", category='error')
            else:
                new_can = can(firstname=firstname, lastname=lastname, email=email, manifesto=manifesto, post=str_choice )
                db.session.add(new_can)
                db.session.commit()
                flash("details have been uploaded", category='success')

        elif str_choice == 'vice-president':

            if can2.query.filter_by(email=email).first():
                flash("email already exists!", category='error')

            else:
                new_vice = can2(firstname=firstname, lastname=lastname, email=email, manifesto=manifesto, post=str_choice )
                db.session.add(new_vice)
                db.session.commit()
                flash("details have been uploaded", category='success')

        return render_template("adminLogin.html", user=current_user, data=post)

    return render_template("admin_maintain.html", user=current_user)


@auth.route('/Vote', methods=['GET', 'POST'])
@login_required
def vote():

    data = db.session.query(can.firstname, can.lastname, can.manifesto).all()

# id of current user = user_id

    user_id = current_user.id
    print("current user id:", user_id)

# checks for the id of all stored polling id

    poll_chck = db.session.query(poll.poll_id).all()
    print("poll check", poll_chck)
    print("next is post method")

# polling id is the id of current user in the database

    # polling_id = db.session.query(poll).where(poll.poll_id == user_id).first()
    # print("polling id:", polling_id)

    vt_ch = db.session.query(students.has_voted).filter(students.id == user_id).where(students.has_voted == 0).first()
    print("this is the value:", vt_ch)

    if request.method == 'POST':

        try:

            vt_ch == 1

            # to check if user has voted

            # session["picked_ses"] = picked

            # if "picked_ses" in session:
            flash("you have already voted!", category='error')
            #    return redirect(url_for('auth.logout'))
        except:

            # sends post request from button
            picked = request.form['vote_btn']

            db.session.execute(update(students).where(students.id == current_user.id).values(has_voted=1))

            db.session.execute(update(students).where(students.id == current_user.id).values(choice=picked))

            x = can.vote_count
            x = x + 1

            db.session.execute(update(can).where(can.firstname == picked).values(vote_count=x))

            flash('Thanks for voting for the president post!', category='success')

            db.session.commit()

            return redirect(url_for('auth.vice'))

        # return render_template("vice.html", user=current_user)

    return render_template("Vote.html", user=current_user, data=data)

    return render_template("Vote.html", user=current_user, data=data)


@auth.route('/vice', methods=['GET', 'POST'])
@login_required
def vice():

    data1 = db.session.query(can2.firstname, can2.lastname, can2.manifesto).all()
    # for vicef, vicel, vices_man in data1:
    #    print(vicef, vicel, vices_man)

    user_id = current_user.id
    print("current user id:", user_id)

    vt_ch = db.session.query(students.has_voted).filter_by(id = user_id).where(students.has_voted == 0).first()
    print("this is the value:",vt_ch)

    # sends post request from button
    if request.method == 'POST':

        try:

            # to check if user has voted
            vt_ch == 1
            flash("you have already voted!", category='error')
            #    return redirect(url_for('auth.logout'))

            # sends post request from button

        except:

            # after_request()
            picked = request.form['vote_btn']

            db.session.execute(update(students).where(students.id == current_user.id).values(choice2=picked))

            x = can2.vote_count
            x = x + 1

            db.session.execute(update(can2).where(can2.firstname == picked).values(vote_count=x))
            db.session.commit()
            flash("Thanks for voting the vice post!", category='success')
            return redirect(url_for('auth.logout'))

    return render_template("vice.html", user=current_user, data1=data1)

    return render_template("Vice.html", user=current_user, data1=data1)


@auth.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():

    data = db.session.query(can.firstname,can.manifesto, can.post).all()

    data1 = db.session.query(can2.firstname, can2.manifesto, can2.post).all()

    if request.method == "POST":

        picked = request.form['delete_btn']

        trial = can.query.filter_by(firstname=picked).first()
        print(trial)

        trial1 = can.query.filter(can.firstname == picked).first()
        print(trial1)

        dt_ch = db.session.query(can).filter_by(firstname=picked).where(can.firstname == picked).first()
        print("can picked id:", dt_ch)
        # print(dt_ch.id)

        # query for vice

        trial3 = can2.query.filter_by(firstname=picked).first()
        print(trial3)

        trial4 = can2.query.filter(can.firstname == picked).first()
        print(trial4)

        dt_chk = db.session.query(can2).filter_by(firstname=picked).where(can2.firstname == picked).first()
        print("can picked id:", dt_chk)
        # print(dt_chk.id)

        if dt_chk is None:

            try:
                print("trying the first")
                db.session.delete(dt_ch)
                db.session.commit()
                return redirect('delete')

            except:

                flash("The candidate isn't in the president table, try another", category='error')

        else:

            try:

                print("trying the second")
                db.session.delete(dt_chk)
                db.session.commit()
                return redirect('delete')

            except:

                return flash("There was an error in deleting candidate from vice-president")

    else:

        return render_template("delete.html", user=current_user, data=data, data1=data1)

    return render_template("delete.html", user=current_user, data=data, data1=data1)


@auth.route('/help', methods=['GET'])
def help():

    return render_template("help.html", user=current_user)


@auth.route('/forgot', methods=['GET', 'POST'])
def forgot():

    if request.method == 'POST':

        forgot_email = request.form['forgot_email']
        print(forgot_email)

        # try_email = db.session.query(students).filter_by(email=forgot_email).where(students.email == forgot_email).first()

        # dt_chk = db.session.query(can2).filter_by(firstname=picked).where(can2.firstname == picked).first()

        try_email = db.session.query(students).where(students.email == forgot_email).first()

        # try_email = students.query.filter_by(email=forgot_email).first()
        print(try_email)

        session['forgot_email1'] = forgot_email
        # update(forgot_email)

        if try_email is None:
            return flash("Email not found", category='error')

        else:

            flash("Email found, Input new password", category='success')
            return redirect('update_pass')

            # render_template("update_pass", user=current_user, forgot_email=forgot_email)

    return render_template("forgot.html", user=current_user)

    return render_template("forgot.html", user=current_user)


@auth.route('/update_pass', methods=['GET', 'POST'])
def update():

    forgot_email = session.get('forgot_email1', None)
    forgot_emaill = db.session.query(students).where(students.email == forgot_email).first()
    print("this is try email", forgot_emaill)
    print("this is try email id", forgot_emaill.id)

    if request.method == 'POST':

        new_password = request.form.get('new_password')
        new_password2 = request.form.get('new_password2')
        # print(new_password)
        # print(new_password2)

        if new_password != new_password2:

            flash("passwords do not match", category='error')

        elif len(new_password) < 7:

            flash("password must be greater than 7", category='error')

        else:

            try:

                db.session.execute(update(students).where(students.id == forgot_emaill.id).values(password=generate_password_hash(new_password, method='sha256')))
                db.session.commit()
                flash("Password updated successfully")

            except:

                flash("Error updating password")

        return render_template("update_pass.html", user=current_user)

    return render_template("update_pass.html", user=current_user)
