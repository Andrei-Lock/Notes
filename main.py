import os
import sqlite3
import re

import markups as nav
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


async def bd():
	global username
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS {username}_names(Note TEXT)'.replace("{username}", str(username)))


async def content_writer(content, name):
	global username
	f = open(str(name) + ".txt", "w")
	f.write(content)


async def delete_note(name):
	global username
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute('DELETE FROM {username}_names WHERE Note = ?'.replace("{username}", str(username)), (name, ))
	con.commit()
	os.remove(str(name) + ".txt")


async def open_note(name):
	f = open(str(name) + ".txt", "r")
	return f.read()


async def name_writer(name):
	global username
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	mass = []
	mass.append(name)
	cur.execute('INSERT INTO {username}_names VALUES(?)'.replace("{username}", str(username)), mass)
	con.commit()
	cur.close()


async def send_base():
	global username
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	query = 'SELECT * FROM {username}_names WHERE Note IS NOT NULL'.replace("{username}", str(username))
	cur.execute(query)
	data = cur.fetchall()
	if data == []:
		return "Нет заметок"
	mm = []
	for i in data:
		mm.append(i)
	ww = len(data)
	g = []
	for i in range(ww):
		a = re.sub('|\(|\'|\,|\)', '', str(mm[i]))
		g.append(a)
	c = []
	for i in g:
		q = i[:len(i) - len(username)] + "\n"
		c.append(q)
	val = '\n'.join(c)
	return val


TOKEN = "TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
state = 'start'
name = ""
username = ""


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	global username
	username = message.from_user.username
	await bd()
	await bot.send_message(message.chat.id, "Добрый день", reply_markup=nav.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
	global state, name, username
	username = message.from_user.username
	await bd()
	if message.chat.type == 'private':
		if message.text == "Добавить заметку":
			state = 'add_name'
			await bot.send_message(message.chat.id, "Введите название заметки", reply_markup=nav.mainMenu)
		elif message.text == "Мои заметки":
			await bot.send_message(message.chat.id, await send_base())
			state = "open_note"
			await bot.send_message(message.chat.id, "Введите название заметки, которую хотите открыть", reply_markup=nav.mainMenu)
		elif message.text == "Удалить заметку":
			state = 'delete_note'
			await bot.send_message(message.chat.id, "Введите название заметки")
		elif message.text == "⬅ Главное меню":
			await bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=nav.mainMenu)
			state = "start"
		else:
			if state == 'add_name' and message.text != "Введите название заметки":
				myString = message.text + str(message.from_user.username)
				name = message.text
				await name_writer(myString)
				state = "add_content"
				await bot.send_message(message.chat.id, "Введите содержание заметки", reply_markup=nav.mainMenu)
			elif state == 'add_content' and message.text != "Введите содержание заметки":
				myString = message.text
				await content_writer(myString, name + str(message.from_user.username))
				state = "start"
				name = ""
				await bot.send_message(message.chat.id, "Успешно", reply_markup=nav.mainMenu)
			elif state == 'delete_note' and message.text != "Введите название заметки":
				myString = message.text + str(message.from_user.username)
				await delete_note(myString)
				state = "start"
				await bot.send_message(message.chat.id, "Успешно", reply_markup=nav.mainMenu)
			elif state == 'open_note' and message.text != "Введите название заметки, которую хотите открыть":
				myString = message.text + str(message.from_user.username)
				await bot.send_message(message.chat.id, await open_note(myString), reply_markup=nav.mainMenu)
				state = "start"


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
