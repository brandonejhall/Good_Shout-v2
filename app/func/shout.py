from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, json
from app.models import User, Shouts
from app.auth import bp
from app import app, db
from flask_login import current_user , login_user, login_required, logout_user

@login_required
@bp.route('/shout',methods = ['POST','GET'])
def shout():
    if request.method == 'POST':
        
        shout = request.form.get('shout')

        new_shout = Shouts(data=shout,user_id=current_user.id)
        db.session.add(new_shout)
        db.session.commit()
        flash('What a Shout!', category = 'success')


    return render_template("func/shout.html") 

@login_required
@bp.route('/delete-shout', methods=['POST'])
def delete_note():
    shout = json.loads(request.data)
    shoutId = shout['shoutId']
    shout = Shouts.query.get(shoutId)
    if shout:
        if shout.user_id == current_user.id:
            db.session.delete(shout)
            db.session.commit()

    return jsonify({})