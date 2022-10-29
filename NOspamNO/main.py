import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import keyboard as kb
from send import Form, Hu_Tao,User,NewUser,Chat, NewPhone
import db

my_secret = os.environ['Cool']
bot = Bot(token='5591104183:AAGu5ppSRPMYlBsC7kN_8rTG5OJ2E-wUUvY')
dp = Dispatcher(bot,storage=MemoryStorage())
chat_id = -1001626563343

user = {'name': '','phone': '','id_name': '','id_chat': ''}

@dp.message_handler(commands=['start'])
async def start(m: types.Message):
  sqll = [x.user_id for x in db.session.query(db.User.user_id).distinct()]
  sqll1 = [x.user_name for x in db.session.query(db.User.user_name).distinct()]
  sqll2 = [x.phone_number for x in db.session.query(db.User.phone_number).distinct()]
  sqll3 = [x.id_chat for x in db.session.query(db.User.id_chat).distinct()]
  black = [x.id_users for x in db.session.query(db.Black.id_users).distinct()]
  if m.from_user.username in sqll and str(m.chat.id) not in black:
    bilder = ReplyKeyboardMarkup(resize_keyboard=True)
    bilder.add(types.KeyboardButton(
          text="Оставить заявку"),
          types.KeyboardButton(
          text="Настройки"),
          types.KeyboardButton(
          text="Связаться"),
          types.KeyboardButton(
          text="Полезные контакты")
      )
    index_found = sqll.index(m.from_user.username)
    user['id_name'] = sqll[index_found]
    user['name'] = sqll1[index_found]
    user['phone'] = sqll2[index_found]
    user['id_chat'] = sqll3[index_found]
    await m.reply('Добро пожаловать в главное меню чат-бота Управляющей компании "УЭР-ЮГ". Здесь Вы можете оставить заявку для управляющей компании или направить свое предложение по управлению домом.Просто воспользуйтесь кнопками меню, чтобы взаимодействовать с функциями бота:', reply_markup=bilder)
  elif str(m.chat.id) in black:
    await m.reply('Вы забанены')
  else:
    bilder = ReplyKeyboardMarkup()
    bilder.add(types.KeyboardButton(
          text="Регистрация")
      )
    await m.reply('Нажмите кнопку "Регестрация"',reply_markup=bilder)

#######Регистрация###
@dp.message_handler(lambda m: m.text == "Регистрация",state=None)
async def one(m: types.Message):
  await m.reply('''Доброго времени суток, бот создан, чтобы обробатывать заявки и оброщения пользователей. Чтобы воспользоваться этим, пришлите для начала Ваше Имя и Фамилию. ''')
  await User.name.set()

@dp.message_handler(state=User.name)
async def two(m: types.Message,state: FSMContext):
  try:
    async with state.proxy() as data:
      if m.text.split()[1] and m.text.split()[1][0].istitle() and m.text.split()[0][0].istitle():
        data['name'] = m.text
        try:
          data['id_name'] = m.from_user.username
          user['id_name'] = m.from_user.username
        except: 
          data['id_name'] = 'username'
          user['id_name'] = 'username'
        data['id_chat'] = m.chat.id
        data['id'] = m.from_user.id
        user['name'] = m.text
      else:
        await m.reply('',reply_markup=kb.continues())
        
  
    await m.reply('Теперь отправьте Ваш номер телефона через +7 следующим сообщением:')
    await User.next()
  except:
    await m.reply('''Имя и Фамилия должны быть введены через один пробел, и должны быть написаны через кирилицу. Также должны быть заглавные буквы.Учтите формат и попробуйте снова:''')
    

@dp.message_handler(state=User.phone)
async def tre(m: types.Message,state: FSMContext):
  try:
      async with state.proxy() as data:
        if m.text[:2] == '+7' and m.text[2:].isdigit() and len(m.text[1:]) == 11:
          data['phone'] = m.text
          user['phone'] = m.text
    
      users = db.User(user_name=str(data['name']),phone_number=data['phone'],user_id=data['id_name'],id_chat=data['id_chat'],id_users=data['id'])
      db.session.add(users)
      db.session.commit()
      db.session.close()
        
      await m.reply('Отлично. Теперь введите комманду /start, чтобы перезапустить бота.')
      await state.finish()
  except:
    await m.reply('Номер телефона должен содержать 11 цифер и должен обязательно содержать в начале +7.Учтите формат и попробуйте сново:')
#####################
    


@dp.message_handler(lambda m: m.text == "Оставить заявку")
async def request(m: types.Message):
  bilder = InlineKeyboardMarkup()
  bilder.add(types.InlineKeyboardButton(
        text="Оставить заявку",
        callback_data="request_1"),
        types.InlineKeyboardButton(
        text="Поделиться предложением",
        callback_data="hu-tao")
    )
  await m.reply('Выберитк категорию, по которой Вы хотите оставить заявку в УК:',reply_markup=bilder)

####Заявка 1#########
@dp.callback_query_handler(text_startswith='request_1', state='*')
async def request_1(callback: types.CallbackQuery):

  await callback.message.answer('''
  Шаг 1/3 Напишите адрес или орентир проблемы(улицу, номер дома, подъезд, этаж и квартиру):
  ''')

  await Form.why.set()

@dp.message_handler(state=Form.why)
async def whyWhat(m: types.Message,state: FSMContext):
  async with state.proxy() as data:
    data['why'] = m.text
  
  await m.reply('Отлично. Давайте продолжим?',reply_markup=kb.continues('request_2','request_1'))
  await Form.next()

@dp.callback_query_handler(text='request_2',state=Form)
async def request_2(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.answer('''
Шаг 2/3 прикрепите фотографию или видео к своей заявке:
''',reply_markup=kb.NextOrQute('request_1'))

@dp.message_handler(content_types=['photo','video'],state=Form.okay)
async def okayWhat(m: types.Message,state: FSMContext):

  async with state.proxy() as data:
    if m.video:
      data['okay'] = m.video.file_id
    else: data['okay'] = m.photo[0].file_id
  
  await m.reply('Отлично. Давайте продолжим.',reply_markup=kb.continues('request_3','request_1'))
  await Form.next()
  

@dp.callback_query_handler(text='request_3',state=Form)
async def request_3(callback: types.CallbackQuery):
  bilder = InlineKeyboardMarkup()
  bilder.add(types.InlineKeyboardButton(
      text='Назад',
      callback_data="request_2"))

  await callback.message.answer('''
Шаг 3/3 Напишите причину обращения в подробностях:
''',reply_markup=bilder)
  
@dp.message_handler(state=Form.oh)
async def ohWhat(m: types.Message,state: FSMContext):
  async with state.proxy() as data:
    data['oh'] = m.text
  await m.reply('''
  Жалоба отправлена администрации. Спасибо за Ваше обращение!
''')
  
  f = f'Поступила новая жалоба:\n@{user["id_name"]}\nИмя и Фамилия:{user["name"]}\nНомер телефона:{user["phone"]}\nАдрес:{data["why"]}\nСодержание:{data["oh"]}\n\nЧтобы ответить пользователю напешите команду /send {m.from_user.id}'
  
  async with state.proxy() as data:
    try:
      await bot.send_photo(-834023831,
                          photo=data['okay'],
                          caption=f)
    except:
      await bot.send_video(-834023831,
                          video=data['okay'],
                          caption=f)
  await state.finish()

###################################


######Заявка2###########
@dp.callback_query_handler(text='hu-tao',state=None)
async def hu_tao(callback: types.CallbackQuery):
  await callback.message.answer(
    '''Распишите Ваши предложение в подробностях '''
  )
  await Hu_Tao.why.set()

@dp.message_handler(content_types=['text'],state=Hu_Tao.why)
async def send_what(m: types.Message,state: FSMContext):
  async with state.proxy() as data:
    data['why'] = m.text
  
  f = f'Поступила новое предложение:\n@{user["id_name"]}\nИмя и Фамилия:{user["name"]}\nНомер телефона:{user["phone"]}\nСодержание:{data["why"]}\n\nЧтобы ответить пользователю напешите команду /send {m.from_user.id}'
  
  async with state.proxy() as data:
    await bot.send_message(-817291908,f)
  await m.reply('Идея принята и передана администрации. Спасибо за Ваше оброщение!')
  await state.finish()
###################################

#########Настройки################

@dp.message_handler(lambda m: m.text == 'Настройки')
async def setings(m: types.Message):
  await m.reply('Тут Вы сможете поменять Имя и Фамилию в Базе данных нашего бота или же можете поменять Ваш номер телефона, если Вы изначально вводили что-то неверно. Выберите, что хотите поменять.', reply_markup=kb.names('name', 'phone'))

@dp.callback_query_handler(text='name',state=None)
async def name(callback: types.CallbackQuery):
  await callback.message.answer(
    '''Отправь своё Имя и Фамилию, чтобы поменять настройки:'''
  )
  await NewUser.name.set()

@dp.message_handler(content_types=['text'],state=NewUser.name)
async def send_whatt(m: types.Message,state: FSMContext):
  try:   
    if m.text.split()[1] and m.text.split()[1][0].istitle() and m.text.split()[0][0].istitle():
      db.User.update_name(user['name'],m.text)
      await m.reply('Настройки имени успешно применены!')
      await state.finish()
    else:
      await m.reply('',reply_markup=kb.continues())
  except:
    await m.reply('''Имя и Фамилия должны быть введены через один пробел, и должны быть написаны через кирилицу. Также должны быть заглавные буквы.Учтите формат и попробуйте снова:''')

@dp.callback_query_handler(text='phone',state=None)
async def phone(callback: types.CallbackQuery):
  await callback.message.answer(
    '''Отправь свой номер телефона, чтобы поменять настройки:'''
  )
  await NewPhone.phone.set()

@dp.message_handler(content_types=['text'],state=NewPhone.phone)
async def send_whats(m: types.Message,state: FSMContext):
  try:
    if m.text[:2] == '+7' and m.text[2:].isdigit() and len(m.text[1:]) == 11:
      db.User.update_phone(user['name'],m.text)
      await m.reply('Настройки номера успешно применены!')
      await state.finish()
    else:
      await m.reply('',reply_markup=kb.continues())
  except:
    await m.reply('Номер телефона должен содержать 11 цифер и должен обязательно содержать в начале +7.Учтите формат и попробуйте сново:')
##########################

########Связаться с админом#######
@dp.message_handler(lambda m: m.text == "Связаться",state=None)
async def ones(m: types.Message):
  await m.reply('Выберите способ связи из нижеперечислнного списка:',reply_markup=kb.open('send_chat','send_u_phone'))
  
@dp.callback_query_handler(text='send_chat',state=None)
async def send_user(callback: types.CallbackQuery):
  await callback.message.answer('Добрый день! Я - диспетчер управляющей компании "УЭР-ЮГ", готов помоч Вам. Напишите, пожалуйста, интересующий Ваш вопрос и ожидайте',reply_markup=kb.close('send_close'))
  await Chat.chat.set()
  
@dp.message_handler(state=Chat.chat)
async def send_user_1(m: types.Message,state: FSMContext):
  await bot.send_message(chat_id,f'(@{user["id_name"]}/Id-chat{m.from_user.id}){user["name"]} - {m.text}')

@dp.callback_query_handler(text='send_close',state="*")
async def send_close(callback: types.CallbackQuery,state: FSMContext):
  await callback.message.answer('Диалог с администратором завершён...')
  await state.finish() 

@dp.callback_query_handler(text='send_u_phone')
async def send_u_phone(callback: types.CallbackQuery):
  await callback.message.answer(f'Это ваш номер?{user["phone"]}? Если да, нажмите соответствующую кнопку.',reply_markup=kb.newphone('yes'))

@dp.callback_query_handler(text='yes')
async def send_u_phone2(callback: types.CallbackQuery):
  await callback.message.answer('Отлично! Наш диспетчер перезвонит Вам в ближайшее время.')
  await bot.send_message(chat_id,f'(@{user["id_name"]}){user["name"]} - Перезвоните этому номеру {user["phone"]}')
##################################

############Полезные контакт##########
@dp.message_handler(lambda m: m.text == "Полезные контакты")
async def good(m: types.Message):
  await m.reply("""Управляющая компания:\n
Диспетчерская служба ООО «УЭР-ЮГ»\n
+7 472 235-50-06\n
Инженеры ООО «УЭР-ЮГ»\n
+7 920 566-28-86\n
Бухгалтерия ООО «УЭР-ЮГ»\n
+7 472 235-50-06\n
Белгород, Сеято-Троицкий 6-р, д. 15, подъезд
№1\n\n
Телефоны для открытия ворот и
шлагбаум:\n
Шлагбаум «Набережная»\n
+7 920 554-87-74\n
Ворота «Харьковские»\n
+7 920 554-87-40\n
Ворота «Мост»\n
+7 920 554-64-06\n
Калитка 1 «Мост»\n
+7 920 554-42-10\n
Калитка 2 «Мост»\n
+7 920 554-89-04\n
Калитка 3 «Харьковская»\n
+7 920 554-87-39\n
Калитка 4 «Харьковская»\n
+7 920 554-89-02\n\n
Охрана\n
+7 915 57-91-457\n\n
Участковый\n
Куленцова Марина Владимировна\n
+7 999 421-53-72""")
  
######Панель управления######
@dp.message_handler(commands=['users'])
async def send_help(message: types.Message):
    if message.chat.id == -844439269:
        id = [x.id for x in db.session.query(db.User.id).distinct()]
        phone = [x.phone_number for x in db.session.query(db.User.phone_number).distinct()]
        
        name = [x.user_name for x in db.session.query(db.User.user_name).distinct()]
      
        id_name = [x.user_id for x in db.session.query(db.User.user_id).distinct()]
        
        id = [x.id_users for x in db.session.query(db.User.id_users).distinct()]
        
        await bot.send_message(-844439269,"\n".join(f'(@{id_name[i]})(id_chat-{id[i]}){name[i]} - {phone[i]}' for i in range(len(id))))

@dp.message_handler(commands=['send'])
async def send(m: types.Message):
    if m.chat.id == -844439269:
        await bot.send_message(m.get_args(),' '.join(m.text.split()[2:]))

@dp.message_handler(commands=['help'])
async def help(m: types.Message):
  if m.chat.id == -844439269:
    await m.reply('/send - ответить пользователю\n/reply - сделать рассылку среди других пользователей\n/ban и /unban - забанить, разбанить пользователя')

@dp.message_handler(commands=['reply'])
async def replyAll(m: types.Message):
  if m.chat.id == -844439269:
    txt = ' '.join(m.text.split()[1:])
    users = [x.id_chat for x in db.session.query(db.User.id_chat).distinct()]
    for i in users:
      await bot.send_message(i,txt)

@dp.message_handler(commands=['ban'])
async def ban(m: types.Message):
  if m.chat.id == -844439269:
   users = db.Black(id_users=m.get_args())
   db.session.add(users)
   db.session.commit()
   db.session.close()
   await bot.send_message(m.get_args(),'Вас забанили')

@dp.message_handler(commands=['unban'])
async def ban(m: types.Message):
  if m.chat.id == -844439269:
    x = db.session.query(db.Black).filter(db.Black.id_users == m.get_args()).delete()
    db.session.commit()
    await bot.send_message(m.get_args(),'Вас разбаненли')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
