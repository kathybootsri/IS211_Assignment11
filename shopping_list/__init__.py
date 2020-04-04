# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:39:41 2019

@author: kbootsri
"""

import os
from flask import Flask
from flask import (render_template, request, flash, redirect, abort)

#CREATED FREE POSTGRESQL DATABASE USING ELEPHANT SQL TO CLOUD LIST
def get_db():
    import psycopg2
    
    connection = psycopg2.connect(user = "zowglzqx",
                                  password = "HinwKUQSD2t_10zuQK5Tln-us-7N9JsI",
                                  host = "drona.db.elephantsql.com",
                                  database = "zowglzqx")
    
    cursor = connection.cursor()
    
    return cursor

def get_conn():
    import psycopg2
    
    connection = psycopg2.connect(user = "zowglzqx",
                                  password = "HinwKUQSD2t_10zuQK5Tln-us-7N9JsI",
                                  host = "drona.db.elephantsql.com",
                                  database = "zowglzqx")

    return connection

def empty_tasks():
    db = get_db()
    db.execute('SELECT task, email, priority, created, id FROM "public"."shopping_list"  ORDER BY created DESC')
    avail_tasks = db.fetchall()
    return avail_tasks

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True


    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #CREATE GET POST ID FUNCTION FOR NESTED FUNCTION USE
    def get_post(id):
        db = get_db()

        db.execute('SELECT id, task, email, priority, created FROM "public"."shopping_list" WHERE id = %s', [id])
        
        post = db.fetchone()
        
        if post is None:
            abort(404, "Post id {0} doesn't exist.".format(id))
    
        return post

    #TASK: UPDATE
    @app.route('/<int:id>/update', methods=('GET', 'POST'))  
    def update(id):
        post = get_post(id)
    
        if request.method == 'POST':
            task = request.form['task']
            email = request.form['email']
            priority = request.form['priority']
            error = None
    
            if not task:
                error = 'Task is required.'

            if not email:
                error = 'Email is required.'

            if not task:
                priority = 'Priority is required.'
                
            if error is not None:
                flash(error)
            else:
                connection = get_conn()

                cursor = connection.cursor()

                cursor.execute('UPDATE "public"."shopping_list" SET task = %s, email = %s, priority = %s WHERE id = %s', (task, email, priority, id))
                
                connection.commit()
                
                return redirect('/')
    
        return render_template('blog/update.html', post=post)

    #TASK: CREATE
    @app.route('/submit', methods=('GET', 'POST'))
    def create():
        if request.method == 'POST':
            task = request.form['task']
            email = request.form['email']
            priority = request.form['priority']
            error = None
    
            if not task:
                error = 'Task is required.'
                
            if not email:
                error = 'Email is required.'
                
            if not priority:
                error = 'Priority is required.'
                
            if error is not None:
                flash(error)
            else:
                connection = get_conn()
        
                cursor = connection.cursor()
        
                cursor.execute('INSERT INTO "public"."shopping_list" (task, email, priority) VALUES (%s, %s, %s)', (task, email, priority))
                
                connection.commit()
                
                return redirect('/')
    
        return render_template('blog/create.html')


    #TASK: LIST ALL TASKS OR DEFAULT TO CREATE IF NONE
    @app.route('/')
    def index():
        avail_tasks = empty_tasks()
        if avail_tasks is not None:
            db = get_db()
            db.execute('SELECT task, email, priority, created, id FROM "public"."shopping_list"  ORDER BY created DESC')            
            posts = db.fetchall()
            return render_template('blog/index.html', posts=posts)
    
        else: 
            return redirect('/submit')
        
    #TASK: DELETE
    @app.route('/<int:id>/delete', methods=('GET', 'POST'))
    def delete(id):
        get_post(id)
        connection = get_conn()

        cursor = connection.cursor()

        cursor.execute('DELETE FROM "public"."shopping_list" WHERE id = %s', [id])
        connection.commit()

        return redirect('/')

    #TASK: CLEAR ALL
    @app.route('/clear', methods=('GET', 'POST'))
    def clear_all():
        connection = get_conn()

        cursor = connection.cursor()

        cursor.execute('DELETE FROM "public"."shopping_list"')
        connection.commit()

        return redirect('/')    
               
    return app


create_app()

if __name__=='__main__':
    create_app()
