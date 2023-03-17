def user_schema(user_db) -> dict:
    return {"id": str(user_db["_id"]),
            "username": user_db["username"],
            "email": user_db["email"]}

def users_schema(users: list) -> list:
    return [user_schema(user) for user in users]
