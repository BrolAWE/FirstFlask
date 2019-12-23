from datetime import datetime

import math
from flask import render_template, session, redirect, url_for, flash, request
from flask_login import login_required

from app.email import send_email
from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.ﬁlter_by(username=form.name.data).ﬁrst()
        if user is None:
            flash('Новый пользователь!')
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if True:
                send_email("aleksejdelov@gmail.com", 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False), current_time=datetime.utcnow())


@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'


@main.route('/calc1', methods=['GET', 'POST'])
def calc1():
    return render_template('calc1.html')


@main.route('/calc', methods=['GET', 'POST'])
def calc():
    size = request.args.get('siz')
    return render_template('calc.html', ind=int(size))


def shubic(n, k):
    return((math.factorial(k-1)*math.factorial(n-k))/math.factorial(n))


def subsets(S):
    sets = []
    len_S = len(S)
    for i in range(1 << len_S):
        subset = [S[bit] for bit in range(len_S) if i & (1 << bit)]
        sets.append(subset)
    return sets


@main.route('/otv', methods=['GET', 'POST'])
def otv():
    S = []
    size = request.args.get('siz')
    q = 5
    for i in range(int(size)):
        zn=request.args.get(str(i)).strip()
        S.append(["w" + str(i), int(zn)])
    print(S)
    coal = []
    res = []
    for m in subsets(S):
        coal.append(m)
    del coal[0]
    for i in range(len(coal)):
        tmp = 0
        for j in coal[i]:
            tmp += j[1]
        if tmp >= q:
            res.append(coal[i])
    shu = [0] * len(S)
    for i in range(len(S)):
        for j in range(len(res)):
            for k in range(len(res[j])):
                if (res[j][k][0] == S[i][0]):
                    tmp_res = res[j].copy()
                    del tmp_res[k]
                    tmp = 0
                    for kk in tmp_res:
                        tmp += kk[1]
                    if tmp < q:
                        n = len(S)
                        ak = len(res[j])
                        shu[i] += (shubic(n, ak))
    print(shu)
    return render_template('otv.html', otv=shu)
