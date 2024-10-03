import sqlite3 as sq
import src.config

from aiogram.fsm.state import State, StatesGroup

db = sq.connect(src.config.database_path)
cur = db.cursor()


class dist(StatesGroup):
	dist_text = State()


class admin_add(StatesGroup):
	password = State()
	us = State()


class admin_del(StatesGroup):
	password = State()
	us = State()


class headman_add(StatesGroup):
	us = State()


class headman_del(StatesGroup):
	us = State()


class message123(StatesGroup):
	zv = State()
