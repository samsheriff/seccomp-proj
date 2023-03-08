import json

with open("../db/users.json", "r") as users_db:
    users = json.load(users_db)

def user_name(user='sam'):
    return users[user]['name']