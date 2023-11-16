import sqlite3
import datetime


def exists_user(discord_id):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM users WHERE discord_id = ?
        """, (discord_id,))
        return cursor.fetchone() is not None


def add_user(discord_id):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (discord_id, join_time)
            VALUES (?, ?)
        """, (discord_id, datetime.datetime.utcnow()))


def add_pokemon(trainer_id, name, ability, is_shiny):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pokemon (trainer_id, name, ability, is_shiny, catch_time)
            VALUES (?, ?, ?, ?, ?)
        """, (trainer_id, name, ability, is_shiny, datetime.datetime.utcnow()))
