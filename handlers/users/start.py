from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.inline.main_inline import *
from keyboards.inline.menu_button import *
from utils.db_api import database as commands
from loader import dp, bot
from utils.db_api.database import *
import datetime
from aiogram.types import ReplyKeyboardRemove
from geopy.geocoders import Nominatim
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultPhoto, InputMediaPhoto, InlineQueryResultArticle
import re 

from smsaero import SmsAero


SMSAERO_EMAIL = 'berk.2023@bk.ru'
SMSAERO_API_KEY = 'BRkXPMR_20Dvu6DIqU8nzF9dGjCFNPN8'

def generateOTP():
    return random.randint(111111, 999999)

def isValid(s):
    Pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    return Pattern.match(s)

def send_sms(phone: int, message: str) -> dict:
    api = SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
    return api.send(phone, message)

@dp.callback_query_handler(lambda call: call.data.startswith("confirm---"), state='*')
async def confirm_pay(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    order_id = data.split('---')[1]
    order = await get_order(order_id)
    order_details = await get_order_details(order_id)
    markup = await time_keyboard(order.id)
    await call.message.edit_reply_markup(reply_markup=markup)
    text = f"👤 Заказчик: <b>#{order.user.user_id}</b>\n\n📍 Адрес: {order.address}\n"
    for order_detail in order_details:
        text += f"  {order_detail.product.name}✖️{order_detail.count}\n"
    await bot.send_message(chat_id=-810383073, text=text)


@dp.callback_query_handler(lambda call: call.data.startswith("cancel---"), state='*')
async def confirm_pay(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    await call.message.edit_reply_markup(reply_markup=None)
    order_id = data.split('---')[1]
    order = get_order(order_id)
    await bot.send_message(chat_id=order.user.user_id, text="Платеж не подтвержден ❌")


@dp.callback_query_handler(lambda call: call.data.startswith("delivered_confirm"), state='*')
async def confirm_pay(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    await call.message.edit_reply_markup(reply_markup=None)
    order_id = data.split('---')[1]
    order = await get_order(order_id)
    markup = await rate_keyboard(order_id)
    await bot.send_message(chat_id=order.user.user_id, text="Оцените наши услуги", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data.startswith("order_rate"), state='*')
async def confirm_pay(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    await call.message.edit_text("Спасибо за вашу оценку.", reply_markup=None)
    order_id = data.split('-')[1]
    order = await get_order(order_id)
    lang = await get_lang(call.from_user.id)
    markup = await user_menu(lang)
    await bot.send_message(chat_id=call.from_user.id, text="Добро пожаловать в наш бот. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data.startswith("order_time"), state='*')
async def confirm_pay(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    order_id = data.split('-')[1]
    time = data.split('-')[2]
    order = await get_order(order_id)
    if order.service_type != "pick":
        order_details = await get_order_details(order_id)
        await call.message.edit_reply_markup(reply_markup=None)
        text = f"👤 Заказчик: <b>+{order.user.phone}</b>\n\n📍 Адрес: {order.address}\n"
        for order_detail in order_details:
            text += f"  {order_detail.product.name}✖️{order_detail.count}\n"
        markup = await delivered(order.id)    
        await bot.send_message(chat_id=-853613647, text=text, reply_markup=markup)
    await bot.send_message(chat_id=order.user.user_id, text=f"Платеж подтвержден ✅.\nВаш заказ будет готов через {time} минут")

 
@dp.message_handler(lambda message: message.text in ["🏠 Asosiy menyu", "🏠 Главное меню", "🏠 Ana menü"], state='*')
async def go_home(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    markup = await user_menu(lang)
    await message.answer("Добро пожаловать в наш бот. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
    await state.set_state("get_command")
 

@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await add_user(user_id=message.from_user.id, name=message.from_user.first_name, lang="ru")
    user = await get_user(message.from_id)
    if user is not None and user.phone:
        lang = await get_lang(message.from_user.id)
        markup = await user_menu(lang)
        await message.answer("Привет и добро пожаловать в бот Big Sushi Premium. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
        await state.set_state("get_command")
    else:
        markup =await language_keyboard()
        await message.answer(f"Привет и добро пожаловать в бот Big Sushi Premium. Пожалуйста, введите свой номер телефона в формате 7YYYxxxxxxx")
        await state.set_state("get_phone")


@dp.message_handler(state="get_phone")
async def get_language(message: types.Message, state: FSMContext):
    phone = message.text
    if message.text == "⬅️ Назад":
        markup =await language_keyboard()
        await message.answer(f"Привет и добро пожаловать в бот Big Sushi Premium. Пожалуйста, введите свой номер телефона в формате 7YYYxxxxxxx")
        await state.set_state("get_phone")
    else:
        if isValid(phone):
            user = await get_user(message.from_user.id)
            user.check_phone = phone
            otp = generateOTP()
            user.otp = otp
            user.save()
            await state.update_data(otp=otp)
            # send_sms(phone=int(user.check_phone), message = f"Ваш код подтверждения для Big Sushi Premium: {otp}")
            markup = await back_keyboard()
            await message.answer("Введите SMS-код, отправленный на номер телефона 👇", reply_markup=markup)
            await state.set_state("get_phone_cod")
        else:
            markup =await language_keyboard()
            await message.answer(f"Пожалуйста, введите свой номер телефона в формате 7YYYxxxxxxx")
            await state.set_state("get_phone")
            

@dp.message_handler(lambda message: message.text in ["⬅️️ Назад"], state="get_phone_cod")
async def get_language(message: types.Message, state: FSMContext):
    await message.answer(f"Привет и добро пожаловать в бот Big Sushi Premium. Пожалуйста, введите свой номер телефона в формате 7YYYxxxxxxx")
    await state.set_state("get_phone")



@dp.message_handler(lambda message: message.text not in ["⬅️️ Назад"], state="get_phone_cod")
async def get_language(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if message.text == user.otp:
        user.phone = user.check_phone
        user.save()
        lang = await get_lang(message.from_user.id)
        markup = await user_menu(lang)
        await message.answer("Привет и добро пожаловать в бот Big Sushi Premium. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
        await state.set_state("get_command")
    else:
        await message.answer("⚠️ Вы ввели неверный код подтверждения.\nПопробуйте еще раз")
            

@dp.message_handler(lambda message: message.text in ["🛍 Заказать", "⚙️ Настройки", "ℹ️ О нас", "✍️ Обратная связь", "📥  Корзина",  "🗂 История заказов"], state="get_command")
async def get_user_command(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    command = message.text
    if command in ["✍️ Обратная связь"]:
        lang = await get_lang(message.from_user.id)
        markup = await back_keyboard(lang)
        if lang == "uz":
            await message.answer("🖋 O'z fikr-mulohaza, shikoyat yoki takliflaringizni yozing. Yoki ovozli, video yoki foto xabar yuboring", reply_markup=markup)
        elif lang == "en":
            await message.answer("🖋 Write your feedback, complaint or wish. Or send a voice, video or photo message", reply_markup=markup)
        elif lang == "ru":
            await message.answer("🖋 Напишите свой отзыв, жалобу или пожелание. Или отправьте голосовое, видео или фото сообщение", reply_markup=markup)
        await state.set_state("get_feedback")      
    elif command in ["🛍 Заказать"]:
        photo = open('./MAIN.jpg', 'rb')
        markup = await category_keyboard(user_id=message.from_id)
        await message.answer_photo(photo=photo, caption="Выберите нужную категорию 👇",  reply_markup=markup)
        await state.set_state("get_category")
    elif command in ["📥  Корзина"]:
        text = await get_carts(message.from_user.id)
        if text != "⚠️ Ваша корзина пуста":
            markup = await cart_keyboard(user_id=message.from_user.id)
            await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup, parse_mode='HTML')
        else:
            go_m = await go_order()
            markup = await back_keyboard()
            await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
            await bot.send_message(chat_id=message.from_user.id, text="Начать покупки", reply_markup=go_m)
        await state.set_state("get_cart_command")

        await state.set_state("get_cart_command")
    elif command in ["🗂 Buyurtmalar tarixi", "🗂 Order history", "🗂 История заказов"]:
        summa = 0
        orders = await get_orders(message.from_id)
        markup = await user_menu(lang)
        if lang =="ru":
            text = "<b>🛒История ваших заказов</b>\n\n"  
        for order in orders: 
         
            order_details = await get_order_details(order.id)      
            if lang == "ru":
                text += f"<b>🛒 Заказ</b>\n\n🆔 Заказ: <b>#{order.id}</b>\n"\
                f"🕙 Время заказа: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Адрес: {order.address}\n"
                for order_detail in order_details:
                    text += f"  {order_detail.product.name}✖️{order_detail.count}\n"
                    summa += order_detail.product.price * order_detail.count
                text += f"\n<b>Общий: </b>{summa}\n\n"
        await message.answer(text, reply_markup=markup)
    elif command in ["⚙️ Настройки"]:
        markup = await settings_keyboard()
        await message.answer(text="Выберите нужную команду 👇", reply_markup=markup)
        await state.set_state('settings')
        


@dp.message_handler(lambda message: message.text in ["📞 Изменить номер телефона", "⬅️ Назад"], state="settings")
async def settings(message: types.Message, state: FSMContext):
    if message.text == "📞 Изменить номер телефона":
        markup = await back_keyboard()
        user = await get_user(message.from_user.id)
        await message.answer(f"📱 Ваш номер телефона:{user.phone}\n\nПожалуйста, введите свой номер телефона в формате ABCxxxxxxx", reply_markup=markup)
        await state.set_state("get_number")
    elif message.text == "⬅️ Назад":
        lang = await get_lang(message.from_user.id)
        markup = await user_menu(lang)
        if lang == "ru":
            await message.answer("Привет и добро пожаловать в бот Big Sushi Premium. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
        await state.set_state("get_command")


@dp.message_handler(state="get_number")
async def get_number(message:types.Message, state: FSMContext):
    if message.text == "⬅️️ Назад":
        markup = await settings_keyboard()
        await message.answer(text="Выберите нужную команду 👇", reply_markup=markup)
        await state.set_state('settings')
    if message.text != "⬅️️ Назад":
        if isValid(message.text):
            user = await get_user(message.from_user)
            user.phone = message.text
            user.save()
            markup = await user_menu(user.lang)
            await message.answer(text="Номер телефона успешно изменен✅. \nВыберите нужную команду 👇", reply_markup=markup)
            await state.set_state("get_command")    
        else:
            await message.answer(f"Пожалуйста, введите свой номер телефона в формате ABCxxxxxxx")


@dp.message_handler(state="get_feedback", content_types=types.ContentTypes.ANY)
async def get_feedback_message(message: types.Message, state:FSMContext):
    if message.text in ["⬅️️️ Orqaga", "⬅️️️ Back", "⬅️️️ Назад"]:
        lang = await get_lang(message.from_user.id)
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Choose the required button👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Выберите нужную кнопку👇", reply_markup=markup)
        await state.set_state("get_command")
    else:
        await bot.forward_message(message_id=message.id, chat_id=-1001570855404)
        # await message.forward(chat_id=-1001570855404)
        lang = await get_lang(message.from_user.id)
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("Fikr-mulohazangiz uchun tashakkur!", reply_markup=markup)
        elif lang == "en":
            await message.answer("Thanks for your feedback!", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Спасибо за ваш отзыв!", reply_markup=markup)
        await state.set_state("get_command")
        

@dp.message_handler(state="get_command_about")
async def get_command_about(message: types.Message, state: FSMContext):
    if message.text in ["⬅️️️ Назад"]:
        lang = await get_lang(message.from_user.id)
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Choose the required button👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Выберите нужную кнопку👇", reply_markup=markup)
        await state.set_state("get_command")


@dp.message_handler(state="get_service_type")
async def get_command_about(message: types.Message, state: FSMContext):
    user = await get_user(message.from_id)
    lang = await get_lang(message.from_user.id)
    if message.text in ["⬅️ Назад"]:
        text = await get_carts(message.from_id)
        if text is not None:
            cart_test = await check_cart(message.from_id)
            if cart_test:
                markup = await cart_keyboard(user_id=message.from_id)
                await message.answer(text=text, reply_markup=markup, parse_mode='HTML')
            else:
                go_m = await go_order()
                markup = await back_keyboard()
                await message.answer(text, reply_markup=markup)
                await message.answer("Начать покупки", reply_markup=go_m)
        await state.set_state("get_cart_command")
    elif message.text in ["🏃‍♂️ Самовывоз"]:
        order_type = "pick"
        date = datetime.datetime.now()
        await state.update_data(order_type=order_type)
        order = await add_order(user_id=message.from_id, date=date)
        order.service_type = order_type
        await state.update_data(order_id=order.id)
        carts = await get_cart_objects(message.from_id)
        for cart in carts:
            await add_order_detail(order_id=order.id, product_id=cart.product.id, count=cart.count)
        order_deails = await get_order_details(order.id) 
        summa = 0
        markup = await order_confirmation(lang)
        text = f"<b>🛒Ваш заказ</b>\n\n🆔 Заказ: <b>#{order.id}</b>\nТип заказа: <b>Самовывоз</b>\n"\
        f"👤 Заказчик: <b>#{order.user.user_id}</b>\n"
        for order_detail in order_deails:
            text += f"  {order_detail.product.name}✖️{order_detail.count}\n"
            summa += order_detail.product.price * order_detail.count
        text += f"\n<b>Общая сумма: </b>{summa} ₽"
        text += "\n\nВы можете забрать свою еду через с Метро Озёрная, ул. Никулинская, 13"
        order.summa = summa
        order.save()
        await message.answer(text, reply_markup=markup)
        await state.set_state("confirm_order")
    elif message.text in ["🚚 Доставка"]:
        text = await get_carts(message.from_user.id)
        order_type = "deliver"
        await state.update_data(order_type=order_type)
        lang = await get_lang(message.from_user.id)
        text = []
        if lang == 'uz':
            text = ['Yetkazish manzilini jo\'nating']
        elif lang == 'ru':
            text = ['📍 Отправьте адрес доставки\n\nОтправьте название улицы, номер дома, номер подъезда, номер квартиры и номер домофона']
        elif lang == 'en':
            text = ['Please send your delivery address']
        markup = await location_send(lang)
        await message.answer(text=f"{text[0]} 👇", reply_markup=markup)
        await state.set_state("get_address")
    else:
        pass        


@dp.message_handler(lambda message: message.text in ["❌ Отмена заказа"], state="get_payment", content_types=types.ContentTypes.TEXT)
async def get_command_about(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    if message.text in ["❌ Отмена заказа"]:
        markup = await user_menu(lang)
        await message.answer(text="Главное меню. Выберите нужный раздел 👇", reply_markup=markup)
        await state.set_state("get_command")
    

@dp.callback_query_handler(state="get_category")
async def get_command_about(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    await call.message.delete()
    if call.data == 'back':
        markup = await user_menu(lang)
        await bot.send_message(chat_id=call.from_user.id, text="Главное меню. Выберите нужный раздел 👇", reply_markup=markup)
        await state.set_state("get_command")
    elif call.data == 'go_cart':
        text = await get_carts(call.from_user.id)
        if text != "⚠️ Ваша корзина пуста":
            markup = await cart_keyboard(user_id=call.from_user.id)
            await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup, parse_mode='HTML')
        else:
            go_m = await go_order(lang)
            markup = await back_keyboard(lang)
            await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup)
            await bot.send_message(chat_id=call.from_user.id, text="Начать покупки", reply_markup=go_m)
        await state.set_state("get_cart_command")

    else:
        category = await get_category(call.data)
        markup = await product_keyboard(cat_id=call.data)
        if category.image:
            photo = open(f'.{category.ImageURL}', 'rb')
            if lang == "uz":
                await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Kerakli taomni tanlang 👇", reply_markup=markup)
            elif lang == "en":
                await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Choose the food you want 👇", reply_markup=markup)
            elif lang == "ru":
                await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="İstediğiniz yemeği seçin 👇", reply_markup=markup)
        else:
            if lang == "uz":
                await bot.send_message(chat_id=call.from_user.id, text="Kerakli taomni tanlang 👇", reply_markup=markup)
            elif lang == "en":
                await bot.send_message(chat_id=call.from_user.id, text="Choose the food you want 👇", reply_markup=markup)
            elif lang == "ru":
                await bot.send_message(chat_id=call.from_user.id, text="İstediğiniz yemeği seçin 👇", reply_markup=markup)
        await state.set_state("get_product")
        

@dp.callback_query_handler(state="get_product")
async def get_command_about(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    await call.message.delete()
    if call.data == 'back':
        markup = await category_keyboard(user_id=call.from_user.id)
        if lang == "uz":
            await bot.send_message(chat_id=call.from_user.id, text="Kerakli kategoriyani tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await bot.send_message(chat_id=call.from_user.id, text="Choose a category 👇", reply_markup=markup)
        elif lang == "ru":
            await bot.send_message(chat_id=call.from_user.id, text="İstediğiniz kategoriyi seçin 👇", reply_markup=markup)
        # await state.update_data(order_type=order_type)
        await state.set_state("get_category")
    else:
        product = await get_product(call.data)
        user = await get_user(call.from_user.id)
        cart = await add_cart(user=user, product=product)
        await state.update_data(cart_id=cart.id)
        markup = await order_keyboard(lang=lang, cart_id=cart.id)   
        if product.image:
            photo = open(f'.{product.ImageURL}', 'rb')
            text = f"{product.name}\n\n {product.description}"
            await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=text, reply_markup=markup)
        else:
            await bot.send_message(chat_id=call.from_user.id, text="Выберите еду, которую вы хотите 👇", reply_markup=markup)
        await state.set_state("cart_state")

    
@dp.callback_query_handler(state="cart_state")
async def cart_state(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    command = call.data.split('-')[0]
    cart_id = call.data.split('-')[1]
    if command == "cancel":
        cart = await get_cart(cart_id)
        await call.message.delete()
        markup = await product_keyboard(lang, cat_id=cart.product.category.id)
        category = cart.product.category
        if category.image:
            photo = open(f'.{category.ImageURL}', 'rb')
            if lang == "uz":
                await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Kerakli taomni tanlang 👇", reply_markup=markup)
            elif lang == "en":
                await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Choose the food you want 👇", reply_markup=markup)
            elif lang == "ru":
                await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="İstediğiniz yemeği seçin 👇", reply_markup=markup)
        else:
            if lang == "uz":
                await bot.send_message(chat_id=call.from_user.id, text="Kerakli taomni tanlang 👇", reply_markup=markup)
            elif lang == "en":
                await bot.send_message(chat_id=call.from_user.id, text="Choose the food you want 👇", reply_markup=markup)
            elif lang == "ru":
                await bot.send_message(chat_id=call.from_user.id, text="İstediğiniz yemeği seçin 👇", reply_markup=markup)
        await state.set_state("get_product")
    elif command == "cart_plus":
        cart = await get_cart(cart_id)
        cart.count += 1
        cart.save()
        markup = await order_keyboard(lang=lang, cart_id=cart.id)
        if lang == "uz":
            await call.message.edit_reply_markup(reply_markup=markup)
        elif lang == "en":
            await call.message.edit_reply_markup(reply_markup=markup)
        elif lang == "ru":
            await call.message.edit_reply_markup(reply_markup=markup)
    elif command == "cart_minus":
        cart = await get_cart(cart_id)
        if cart.count <= 1:
            cart.count = 1
        else:
            cart.count -= 1
        cart.save()
        markup = await order_keyboard(lang=lang, cart_id=cart.id)
        await call.message.edit_reply_markup(reply_markup=markup)
    elif command == "confirm":
        cart = await get_cart(cart_id)
        cart.confirm = True
        cart.save()
        await call.message.delete()
        markup = await category_keyboard(user_id=call.from_user.id)
        await bot.send_message(chat_id=call.from_user.id, text="Заказ добавлен в корзину.\nВыберите нужную категорию 👇", reply_markup=markup)
        await state.set_state("get_category")
        

@dp.callback_query_handler(state="get_cart_command")
async def get_cart_query(call:types.CallbackQuery, state:FSMContext):
    lang = await get_lang(call.from_user.id)
    await call.message.delete()
    markup = await category_keyboard(user_id=call.from_user.id)
    photo = open('./MAIN.jpg', 'rb')
    await bot.send_message(chat_id=call.from_user.id, text='.', reply_markup=ReplyKeyboardRemove())
    await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Выберите нужную категорию 👇", reply_markup=markup)
    await state.update_data(order_type=order_type)
    await state.set_state("get_category")
    

@dp.message_handler(state="get_cart_command")
async def get_count(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    if message.text in ["🗑 Savatchani tozalash", "🗑 Clear cart", "🗑 Очистить корзину"]:
        await clear_cart(message.from_id)
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("🗑 Savatcha tozalandi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("🗑 Корзина очищена. Выберите нужный раздел👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("🗑 Cart cleared. Please select the desired section 👇", reply_markup=markup)
        await state.set_state("get_command")
    elif message.text in ["⬅️️ Orqaga", "⬅️️ Back", "⬅️️ Назад"]:
        lang = await get_lang(message.from_user.id)
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Choose the required button👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Выберите нужную кнопку👇", reply_markup=markup)
        await state.set_state("get_command")
    elif message.text in ["🛒 Buyurtmani rasmiylashtirish", "🛒 Complete order", "🛒 Завершить заказ"]:
        markup = await order_type()
        await message.answer(text="Выберите тип услуги", reply_markup=markup)
        await state.set_state("get_service_type")
    else:
        product_name = message.text.split("❌ ")
        try:
            product = await get_product_by_name(product_name[1])
        except:
            pass
        if product is not None:
            await delete_cart_item(product=product, user_id=message.from_user.id)
            text = await get_carts(message.from_id)
            markup = await user_menu(lang)
            if text is not None:
                markup = await cart_keyboard(user_id=message.from_id)
                await message.answer(text=text, reply_markup=markup, parse_mode='HTML')
                await state.set_state("get_cart_command")
            else:
                if lang == "uz":
                    await message.answer("❌ Savatchangiz bo'sh. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
                elif lang == "ru":
                    await message.answer("❌ Ваша корзина пуста. Выберите нужный раздел👇", reply_markup=markup)
                elif lang == "en":
                    await message.answer("❌ Your shopping cart is empty. Please select the desired section 👇", reply_markup=markup)
                await state.set_state("get_command")



# @dp.message_handler(content_types=types.ContentType.LOCATION, state='get_address')
# async def get_location_address(message: types.Message, state: FSMContext):
#     location = message.location
#     geolocator = Nominatim(user_agent="geoapiExercises")
#     Latitude = str(location.latitude)
#     Longitude = str(location.longitude)
#     location = geolocator.geocode(Latitude + "," + Longitude)
#     data = location.raw.get('display_name')
#     data = data.split(',')
#     name = f"{data[0]} {data[1]} {data[2]}"
#     user = await get_user(message.from_user.id)
#     lang = user.lang
#     text = []
#     if lang == 'uz':
#         text = '🔰 Manzilni tasdiqlaysizmi?'
#     elif lang == 'ru':
#         text = '🔰 Вы подтверждаете адрес?'
#     elif lang == 'en':
#         text = '🔰 Do you confirm the location?'
#     await state.update_data(latitude=Latitude, longitude=Longitude, name=name,
#                             display_name=location.raw.get('display_name'))
#     await message.answer(text=location.raw.get('display_name'), reply_markup=ReplyKeyboardRemove())
#     markup = await confirm_address(lang)
#     await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
#     await state.set_state('confirm_address')


@dp.message_handler(content_types=types.ContentType.TEXT, state='get_address')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    command = message.text
    if command == "⬅️ Назад":
        text = await get_carts(message.from_id)
        if text is not None:
            cart_test = await check_cart(message.from_id)
            if cart_test:
                markup = await cart_keyboard(user_id=message.from_id)
                await message.answer(text=text, reply_markup=markup, parse_mode='HTML')
            else:
                go_m = await go_order()
                markup = await back_keyboard()
                await message.answer(text, reply_markup=markup)
                await message.answer("Начать покупки", reply_markup=go_m)
        await state.set_state("get_cart_command")
    elif command == '🔂 Предыдущие адреса':
        locations = await get_address(message.from_user.id)
        if locations:
            user = await get_user(message.from_user.id)
            lang = user.lang
            text = []
            if lang == 'uz':
                text = ['Kerakli mazilni tanlang', 'Manzillar']
            elif lang == 'ru':
                text = ['Выберите нужное место', 'Адреса']
            elif lang == 'en':
                text = ['Choose the desired mazil', 'Addresses']
            markup = await location_keys(user_id=message.from_user.id, lang=lang)
            await message.answer(text=text[1], reply_markup=ReplyKeyboardRemove())
            await bot.send_message(text=text[0], chat_id=message.from_user.id, reply_markup=markup)
            await state.set_state('get_location')
        elif command != '🔂 Предыдущие адреса' and message.text !="⬅️ Назад":
            user = await get_user(message.from_user.id)
            lang = user.lang
            text = []
            if lang == 'uz':
                text = '🗑 Manzillar ro\'yxati bo\'sh'
            elif lang == 'ru':
                text = '🗑 Список адресов пустой'
            elif lang == 'en':
                text = '🗑 The address list is empty'
            await message.answer(text)
    else:
        text = '🔰 Вы подтверждаете адрес?'
        await state.update_data(location_name=message.text)
        await message.answer(text=message.text, reply_markup=ReplyKeyboardRemove())
        markup = await confirm_address(lang)
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
        await state.set_state('confirm_address')

        
@dp.message_handler(content_types=types.ContentType.TEXT, state='get_location')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    if message.text == '⬅️ Назад':
        lang = await get_lang(message.from_user.id)
        text = ['Yetkazish manzilini jo\'nating']
        markup = await location_send(lang)
        await message.answer(text=f"{text[0]} 👇", reply_markup=markup)
        await state.set_state("get_address")
    else: 
        location = await get_location_by_name(name=message.text, user_id=message.from_id)
        if location is not None:
            name = location.name
            user = await get_user(message.from_user.id)
            lang = user.lang
            text = []
            if lang == 'uz':
                text = '🔰 Manzilni tasdiqlaysizmi?'
            elif lang == 'ru':
                text = '🔰 Вы подтверждаете адрес?'
            elif lang == 'en':
                text = '🔰 Do you confirm the location?'
            await state.update_data(location_name=name)
            await message.answer(text=name, reply_markup=ReplyKeyboardRemove())
            markup = await confirm_address(lang)
            await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
            await state.set_state('confirm_address')

@dp.message_handler(content_types=types.ContentType.TEXT, state='confirm_address')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    if message.text in ["⬅️️ Orqaga", "⬅️️ Back", "⬅️️ Назад"]:
        markup = await pay_method(lang)
        if lang == "uz":
            await message.answer("Iltimos to'lov usulini tanlang 👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("Please select a payment method 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Пожалуйста, выберите способ оплаты 👇", reply_markup=markup)
        await state.set_state("get_payment_method")
    elif message.text in ["✅ Tasdiqlash", "✅ Подтвердить", "✅ Confirm"]:
        data = await state.get_data()
        user = await get_user(message.from_user.id)
        location_name = data['location_name']
        order_type = data['order_type']
        date = datetime.datetime.now()
        order = await add_order(user_id=message.from_id, date=date, address= location_name)
        await state.update_data(order_id=order.id)
        order.address = location_name
        carts = await get_cart_objects(message.from_id)
        for cart in carts:
            await add_order_detail(order_id=order.id, product_id=cart.product.id, count=cart.count)
        order_deails = await get_order_details(order.id) 
        summa = 0
        await add_address(user_id=message.from_user.id, name=location_name)
        markup = await order_confirmation(lang)
        text = f"<b>🛒Ваш заказ</b>\n\n🆔 Заказ: <b>#{order.id}</b>\n"\
        f"👤 Заказчик: <b>#{order.user.user_id}</b>\n📍 Адрес: {order.address}\n"
        for order_detail in order_deails:
            text += f"  {order_detail.product.name}✖️{order_detail.count}\n"
            summa += order_detail.product.price * order_detail.count
        text += f"\n<b>Общий: </b>{summa}"
        order.summa = summa
        order.service_type = order_type
        order.save()
        await message.answer(text, reply_markup=markup)
        await state.set_state("confirm_order")
    elif message.text in ["🔄 Qayta jo\'natish", "🔄 Отправить повторно", "🔄 Send again"]:
        lang = await get_lang(message.from_user.id)
        text = []
        if lang == 'uz':
            text = ['Yetkazish manzilini jo\'nating']
        elif lang == 'ru':
            text = ['Отправьте адрес доставки']
        elif lang == 'en':
            text = ['Please send your delivery address']
        markup = await location_send(lang)
        await message.answer(text=f"{text[0]} 👇", reply_markup=markup)
        await state.set_state("get_address")


@dp.message_handler(content_types=types.ContentType.TEXT, state='confirm_order')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    data = await state.get_data()
    # card_type = data["card_type"]
    if message.text in ["❌ Bekor qilish", "❌ Cancel", "❌ Отмена"]:
        await clear_cart(message.from_id)
        order_id = data['order_id']
        order = await get_order(order_id)
        order.delete()
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("🗑 Savatcha tozalandi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("🗑 Корзина очищена. Выберите нужный раздел👇", reply_markup=markup)
        elif lang == "en":
            await message.answer("🗑 Cart cleared. Please select the desired section 👇", reply_markup=markup)
        await state.set_state("get_command")
    elif message.text in ["✅ Подтвердить заказ", "✅ Buyurtmani tasdiqlash", "✅ Confirm order"]:
        text = await get_carts(message.from_user.id)
        data = await state.get_data()
        order_id = data['order_id'] 
        order = await get_order(order_id)
        order_details = await get_order_details(order_id)
        if order.service_type == "deliver":
            markup = await cancel_order()
            await message.answer(text=text + "\n\nОтправьте подтверждение оплаты.\nНомер карты \n<b>2202206269993650</b>", reply_markup=markup)
            await state.update_data(order_type=order_type)
            await state.set_state("get_payment")
        if order.service_type == 'pick':
            summa = 0
            await clear_cart(message.from_user.id)
            text = f"👤 Заказчик: <b>#{order.user.user_id}</b>\n📞 Tелефон: <b>+{order.user.phone}</b>\nТип заказа: <b>Самовывоз</b>\n"
            markup = await confirm_payment(order_id)
            for order_detail in order_details:
                text += f"  {order_detail.product.name}✖️{order_detail.count}\n"
                summa += order_detail.product.price * order_detail.count
            text += f"\n<b>Общая сумма: </b>{summa} ₽"    
            await bot.send_message(chat_id=-883764749, text=text, reply_markup=markup)
            markup = await user_menu("ru")
            
            await message.answer(text="Ваш платеж отправлен на подтверждение")
            await message.answer(text="Главное меню. Выберите нужный раздел 👇", reply_markup=markup)
            await state.set_state("get_command")


@dp.message_handler(state="get_payment", content_types=types.ContentTypes.PHOTO)
async def get_payment_confirm(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    await clear_cart(message.from_user.id)
    order_id = data['order_id']
    markup = await confirm_payment(order_id)
    order = await get_order(order_id)
    order_details = await get_order_details(order_id)
    summa = 0
    text = f"👤 Заказчик: <b>#{order.user.user_id}</b>\n📞 Tелефон: <b>+{order.user.phone}</b>\n📍 Адрес: {order.address}\n"
    for order_detail in order_details:
        text += f"  {order_detail.product.name}✖️{order_detail.count}\n"
        summa += order_detail.product.price * order_detail.count
    text += f"\n<b>Общая сумма: </b>{summa} ₽"    
    await bot.send_photo(chat_id=-883764749, photo=photo, caption=text, reply_markup=markup)
    markup = await user_menu("ru")
    
    await message.answer(text="Ваш платеж отправлен на подтверждение")
    await message.answer(text="Главное меню. Выберите нужный раздел 👇", reply_markup=markup)
    await state.set_state("get_command")

