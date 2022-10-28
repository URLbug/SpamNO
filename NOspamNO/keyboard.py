from aiogram import types
from aiogram.types import InlineKeyboardMarkup


def NextOrQute(qute):
  bilder = InlineKeyboardMarkup()
  bilder.add(
        types.InlineKeyboardButton(
        text="Назад",
        callback_data=qute)
    )
  return bilder   

def continues(a,b):
  bilder = InlineKeyboardMarkup()
  bilder.add(types.InlineKeyboardButton(
      text='Продолжить',
      callback_data=a),types.InlineKeyboardButton(
      text='Назад',
      callback_data=b))
  return bilder

def names(a,b):
  bilder = InlineKeyboardMarkup()
  bilder.add(types.InlineKeyboardButton(
      text='Поменять имя',
      callback_data=a),types.InlineKeyboardButton(
      text='Сменить номер',
      callback_data=b))
  return bilder

def close(a):
  bilder = InlineKeyboardMarkup()
  bilder.add(types.InlineKeyboardButton(
      text='Завершить диалог',
      callback_data=a))
  return bilder

def open(a,b):
  bilder = InlineKeyboardMarkup()
  bilder.add(types.InlineKeyboardButton(
      text='Свяжитесь со мной через чат бота',
      callback_data=a),
      types.InlineKeyboardButton(
      text='Перезвоните мне',
      callback_data=b))
  return bilder

def newphone(a):
  bilder = InlineKeyboardMarkup()
  bilder.add(types.InlineKeyboardButton(
      text='Да',
      callback_data=a))
  return bilder