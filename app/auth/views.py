from flask import render_template, flash, redirect, request, url_for
from flask_login import logout_user, login_required
from flask_login import login_user
from app.auth.forms import LoginForm
from app.models import User
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.ﬁlter_by(email=form.email.data).ﬁrst()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
        return render_template('auth/login.html', form=form)
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


