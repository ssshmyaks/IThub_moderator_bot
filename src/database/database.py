import sqlite3 as sq
import aiosqlite
from src import config

db = sq.connect(config.database_path)
cur = db.cursor()

cur.execute('''  
    CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY,
    tg INTEGER
    )''')

DATABASE_PATH = 'src/database/banwords.db'

# with sq.connect('database.db'):
# 	cur.execute("INSERT INTO admin (tg) VALUES (?)", (825627855,))
# 	db.commit()


def get_admin():
    cur.execute("SELECT tg FROM admin")
    result = cur.fetchall()

    id_list = [row[0] for row in result]

    return id_list


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_bans (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                username TEXT,
                ban_count INTEGER DEFAULT 0
            )
        ''')
        await db.commit()


async def get_user(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT user_id, username, ban_count FROM user_bans WHERE user_id = ?', (user_id,)) as cursor:
            return await cursor.fetchone()


async def add_or_update_user(user_id: int, username: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        user = await get_user(user_id)
        if user:
            ban_count = user[2] + 1
            await db.execute('UPDATE user_bans SET ban_count = ?, username = ? WHERE user_id = ?', (ban_count, username, user_id))
        else:
            ban_count = 1
            await db.execute('INSERT INTO user_bans (user_id, username, ban_count) VALUES (?, ?, ?)', (user_id, username, ban_count))
        await db.commit()
    return ban_count


async def get_all_banned_users():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT user_id, username, ban_count FROM user_bans ORDER BY ban_count DESC') as cursor:
            return await cursor.fetchall()
