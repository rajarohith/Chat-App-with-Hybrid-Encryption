from bson.json_util import dumps
from flask import Flask, render_template, request, redirect, url_for,jsonify,make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, join_room, leave_room
from pymongo.errors import DuplicateKeyError
from dbqueries import *
from enc_dec import encrypt,decrypt

app = Flask(__name__)
app.secret_key = "sfdjkafnk"
sktio = SocketIO(app)
Login_mngr = LoginManager()
Login_mngr.login_view = 'login'
Login_mngr.init_app(app)


@app.route('/')
def home():
    rooms = []
    if current_user.is_authenticated:
        rooms = fetch_rooms_for_user(current_user.username)
    return render_template("main.html",rooms=rooms)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user_data(username)

        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = 'Invalid username or password'
    return render_template('login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            insert_user_data(username, email, password)
            return redirect(url_for('login'))
        except DuplicateKeyError:
            message = "User already exists!"
    return render_template('signup.html', message=message)
@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
@sktio.on('send_message')
def handle_send_message_event(data):
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    data['message'] = encrypt(data['message'])
    insert_message(data['room'], data['message'], data['username'])
    data['message'] = decrypt(data['message'])
    sktio.emit('receive_message', data, room=data['room'])

@app.route('/create_room/', methods=['GET', 'POST'])
@login_required
def create_room():
    message = ''
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        usernames = [username.strip() for username in request.form.get('members').split(',')]

        if len(room_name) and len(usernames):
            room_id = insert_room_data(room_name, current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)
            add_room_members(room_id, room_name, usernames, current_user.username)
            return redirect(url_for('view_room', room_id=room_id))
        else:
            message = "Failed to create room"
    return render_template('create_room.html', message=message)
@app.route('/rooms/<room_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_room(room_id):
    room = fetch_room_data(room_id)
    room_members_str = ""
    if room and is_room_admin(room_id, current_user.username):
        existing_room_members = [member['_id']['username'] for member in fetch_room_members(room_id)]
        room_members_str = ",".join(existing_room_members)
        message = ''
        if request.method == 'POST':
            room_name = request.form.get('room_name')
            room['name'] = room_name
            update_room(room_id, room_name)

            new_members = [username.strip() for username in request.form.get('members').split(',')]
            members_to_add = list(set(new_members) - set(existing_room_members))
            members_to_remove = list(set(existing_room_members) - set(new_members))
            if len(members_to_add):
                add_room_members(room_id, room_name, members_to_add, current_user.username)
            if len(members_to_remove):
                remove_room_members(room_id, members_to_remove)
            message = 'Room updated successfully'
            room_members_str = ",".join(new_members)
        return render_template('edit_room.html', room=room, room_members_str=room_members_str, message=message)
    else:
        if not room:
            return "Room not found", 404
        else:
            message="u don't have the permission to edit this room"
            return render_template('edit_room.html', room=room, room_members_str=room_members_str, message=message)

@app.route('/rooms/<room_id>/')
@login_required
def view_room(room_id):
    room = fetch_room_data(room_id)
    if room and is_room_member(room_id, current_user.username):
        room_members = fetch_room_members(room_id)
        messages = fetch_messages(room_id)
        for i in messages:
            i['text']=decrypt(i['text'])
        return render_template('view_room.html', username=current_user.username, room=room, room_members=room_members,
                               messages=messages)
    else:
        return "Room not found", 404
@app.route('/rooms/<room_id>/messages/')
@login_required
def get_older_messages(room_id):
    room = fetch_room_data(room_id)
    if room and is_room_member(room_id, current_user.username):
        page = int(request.args.get('page', 0))
        messages = fetch_messages(room_id, page)
        for i in messages:
            i['text']=decrypt(i['text'])
        return dumps(messages)
    else:
        return "Room not found", 404

@sktio.on('joined_room')
def handle_join_room_event(data):
    join_room(data['room'])
    sktio.emit('joined_room_action', data, room=data['room'])

@sktio.on('left_room')
def handle_leave_room_event(data):
    leave_room(data['room'])
    sktio.emit('left_room_action', data, room=data['room'])

@Login_mngr.user_loader
def load_user(username):
    return get_user_data(username)


if __name__ == '__main__':
    sktio.run(app, debug=True)

