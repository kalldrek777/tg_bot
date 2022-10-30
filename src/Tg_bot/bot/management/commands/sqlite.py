import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('new.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, subscribe TEXT)")

    db.commit()


async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?,?)", (user_id, 'subscribed'))
        db.commit()


async def get_users():
    return cur.execute("SELECT * FROM profile").fetchall()


async def delete_profile(user_id):
    cur.execute("DELETE FROM profile WHERE user_id =='{key}'".format(key=user_id))
    db.commit()




# def delete_profile     if ['delete'] delete profile