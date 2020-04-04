# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 15:04:49 2020

@author: kbootsri
"""

from flask import (Blueprint, flash, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from flaskr.db import get_db
import pandas as pd
import json
import datetime

bp = Blueprint('blog', __name__)

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
    
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT s.task, s.email, s.priority, s.created'
        ' FROM shopping_list s'
        ' ORDER BY s.created DESC'
    ).fetchall()
    

#    df = pd.DataFrame(posts, columns = ['Task', 'Email', 'Priority', 'Created'])
    
#    df_list = df.values.tolist()      
    
#    JSONP_data = json.dumps(df_list, default = myconverter)

    return render_template('blog/index.html', posts=posts)



@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        task = request.form['task']
        email = request.form['email']
        priority = request.form['priority']
        error = None

        if not task:
            error = 'Task is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO shopping_list (task, email, priority)'
                ' VALUES (?, ?, ?)',
                (task, email, priority)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id):
    post = get_db().execute(
        'SELECT task, email, priority, created, id FROM shopping_list WHERE id = ?',
        (id)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
        
    return post



@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        task = request.form['task']
        email = request.form['email']
        priority = request.form['priority']
        error = None

        if not task:
            error = 'Task is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE shopping_list SET task = ?, email = ?, priority = ?'
                ' WHERE id = ?',
                (task, email, priority, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE shopping_list WHERE id = ?', (id))
    db.commit()
    return redirect(url_for('blog.index'))