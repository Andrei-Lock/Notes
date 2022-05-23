from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ------ Main Menu ------
btnCreateNote = KeyboardButton('Добавить заметку')
btnOpenNote = KeyboardButton('Мои заметки')
btnDeleteNote = KeyboardButton('Удалить заметку')
btnMain = KeyboardButton('⬅ Главное меню')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnCreateNote, btnOpenNote, btnDeleteNote, btnMain)
