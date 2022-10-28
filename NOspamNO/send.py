from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
  why = State()
  okay = State()
  oh = State()

class Hu_Tao(StatesGroup):
  why = State()

class User(StatesGroup):
  name = State()
  phone = State()

class NewUser(StatesGroup):
  name = State()

class NewPhone(StatesGroup):
  phone = State()


class Chat(StatesGroup):
  chat = State()

class Phones(StatesGroup):
  phone = State()
