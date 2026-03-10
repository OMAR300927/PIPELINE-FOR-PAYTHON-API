from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..modules.services import save, delete
from ..modules.models import Players, Users
from datetime import datetime



user_bp = Blueprint('user', __name__, url_prefix='/users')


# SIGN UP
@user_bp.route('/signUp', methods=['GET', 'POST'])
def signUp_user():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if not username or not password or not email:
            flash('All fields are required')
            return redirect(url_for('user.signUp_user'))

        existing_user = Users.query.filter((Users.username==username)|(Users.email==email)).first()
        if existing_user:
            flash('User with this username or email already exists')
            return redirect(url_for('user.signUp_user'))

        new_user = Users(username=username, email=email)
        new_user.set_password(password)
        save(new_user)
        return redirect(url_for('user.login_user'))

    return render_template('sign-up.html')

    
# LOGIN
@user_bp.route('/login', methods=['GET', 'POST'])
def login_user():
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required')
            return redirect(url_for('user.login_user'))

        existing_user = Users.query.filter_by(username=username).first()
        if existing_user and existing_user.check_password(password):
            session['username'] = existing_user.username
            return redirect(url_for('user.home'))

        flash('Invalid username or password')
        return redirect(url_for('user.login_user'))

    return render_template('login.html')


# LOGOUT
@user_bp.route('/logout')
def logout_user():
    
    session.pop('username', None)

    flash('You have been logged out')

    return redirect(url_for('user.login_user'))


# HOME PAGE with CRUD operations for players
@user_bp.route('/', methods=['GET', 'POST'])
def home():

    if 'username' not in session:
        flash('You need to login')
        return redirect(url_for('user.login_user'))

    if request.method == 'POST':

        player_name = request.form.get('player_name')
        score = int(request.form.get('score'))

        new_player = Players(
            player_name=player_name,
            score=score
        )
            
        save(new_player)

    players = Players.query.order_by(Players.created_date.desc()).all()

    return render_template('home.html', players=players)


@user_bp.route('/delete/<string:player_name>', methods=['POST'])
def delete_player(player_name):

    player = Players.query.get(player_name)

    if player:
        delete(player)
        flash('Player deleted successfully')
        return redirect(url_for('user.home'))

    else:
        flash('Player not found')

    return redirect(url_for('user.home'))


@user_bp.route('/update/<string:player_name>', methods=['GET', 'POST'])
def update_player(player_name):

    player = Players.query.filter_by(player_name=player_name).first()

    if not player:
        flash('Player not found')
        return redirect(url_for('user.home'))
    
    if request.method == 'POST':
        player.player_name = request.form['player_name']
        player.score = int(request.form['score'])
        save(player)
        flash('Player updated successfully')
        return redirect(url_for('user.home'))

    return render_template('update.html', player=player)


    