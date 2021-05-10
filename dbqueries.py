from werkzeug.security import generate_password_hash
from pymongo import MongoClient, DESCENDING
from bson import ObjectId
from datetime import datetime
from user import ClassUser

client = MongoClient("mongodb+srv://MajorProject:majorproject@chatting-app.2mepv.mongodb.net/<dbname>?retryWrites=true&w=majority")

chat_db = client.get_database("ChatDB")
users = chat_db.get_collection("users")
rooms = chat_db.get_collection("rooms")
room_members = chat_db.get_collection("room_members")
messages = chat_db.get_collection("messages")


def insert_user_data(username, email, password):
    password = generate_password_hash(password)
    users.insert_one({'_id': username, 'email': email, 'password': password})


def get_user_data(username):
    user_data = users.find_one({'_id': username})
    return ClassUser(user_data['_id'], user_data['email'], user_data['password']) if user_data else None


def insert_room_data(room_name, created_by):
    room_id = rooms.insert_one(
        {'name': room_name, 'created_by': created_by, 'created_at': datetime.now()}).inserted_id
    add_room_member(room_id, room_name, created_by, created_by, is_room_admin=True)
    return room_id


def update_room(room_id, room_name):
    rooms.update_one({'_id': ObjectId(room_id)}, {'$set': {'name': room_name}})
    room_members.update_many({'_id.room_id': ObjectId(room_id)}, {'$set': {'room_name': room_name}})


def fetch_room_data(room_id):
    return rooms.find_one({'_id': ObjectId(room_id)})


def add_room_member(room_id, room_name, username, added_by, is_room_admin=False):
    room_members.insert_one(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
         'added_at': datetime.now(), 'is_room_admin': is_room_admin})


def add_room_members(room_id, room_name, usernames, added_by):
    room_members.insert_many(
        [{'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
          'added_at': datetime.now(), 'is_room_admin': False} for username in usernames])


def remove_room_members(room_id, usernames):
    room_members.delete_many(
        {'_id': {'$in': [{'room_id': ObjectId(room_id), 'username': username} for username in usernames]}})


def fetch_room_members(room_id):
    return list(room_members.find({'_id.room_id': ObjectId(room_id)}))


def fetch_rooms_for_user(username):
    return list(room_members.find({'_id.username': username}))


def is_room_member(room_id, username):
    return room_members.count_documents({'_id': {'room_id': ObjectId(room_id), 'username': username}})


def is_room_admin(room_id, username):
    return room_members.count_documents(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'is_room_admin': True})


def insert_message(room_id, text, sender):
    messages.insert_one({'room_id': room_id, 'text': text, 'sender': sender, 'created_at': datetime.now()})


fetch_limit = 5


def fetch_messages(room_id, page=0):
    x = page * fetch_limit
    msgs = list(
        messages.find({'room_id': room_id}).sort('_id', DESCENDING).limit(fetch_limit).skip(x))
    for message in msgs:
        message['created_at'] = message['created_at'].strftime("%d %b, %H:%M")
    return msgs[::-1]