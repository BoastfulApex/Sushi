from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from backend.models import *
from utils.db_api.database import *


async def language_keyboard():
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text="🇺🇿 O'zbek tili")
    key2 = KeyboardButton(text="🇺🇸 English")
    key3 = KeyboardButton(text="🇹🇷 Türk")
    keyboard.add(key1, key2, key3)
    keyboard.resize_keyboard = True
    return keyboard


async def user_menu(lang):
    texts = []
    if lang == "ru":
        texts = ["Заказать", "Настройки", "О нас", "Обратная связь", "Корзина", "История заказов"]
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"🛍 {texts[0]}")
    key2 = KeyboardButton(text=f"⚙️ {texts[1]}")
    # key3 = KeyboardButton(text=f"ℹ️ {texts[2]}")
    key4 = KeyboardButton(text=f"✍️ {texts[3]}")
    key5 = KeyboardButton(text=f"📥  {texts[4]}")
    key6 = KeyboardButton(text=f"🗂 {texts[5]}")
    keyboard.add(key1)
    keyboard.add(key5, key6)
    keyboard.add(key2, key4)
    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True
    return keyboard


async def back_keyboard():
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"⬅️️ Назад")
    keyboard.add(key1)
    keyboard.resize_keyboard = True
    return keyboard


async def order_type():
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"🏃‍♂️ Самовывоз")
    key2 = KeyboardButton(text=f"🚚 Доставка")
    key3 = KeyboardButton(text=f"⬅️ Назад")
    keyboard.add(key2, key1)
    keyboard.add(key3)
    keyboard.resize_keyboard = True
    return keyboard


async def settings_keyboard():
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"📞 Изменить номер телефона")
    key2 = KeyboardButton(text=f"⬅️ Назад")
    keyboard.add(key1, key2)
    keyboard.resize_keyboard = True
    return keyboard


# async def category_keyboard(lang):
#     texts = []
#     categories = Category.objects.all()
#     texts = []
#     size = len(categories)
#     keyboard = ReplyKeyboardMarkup()
#     for i in categories:
#         if lang == "uz":
#             texts = ["Asosiy menyu", "Orqaga"]
#             keyboard.add(KeyboardButton(text=f"{i.name_uz}"))
#         elif lang == "en":
#             texts = ["Main menu", "Back"]
#             keyboard.add(KeyboardButton(text=f"{i.name_en}"))
#         elif lang == "tr":
#             texts = ["Главное меню", "Назад"]
#             keyboard.add(KeyboardButton(text=f"{i.name_ru}"))
#     back_key = KeyboardButton(f"⬅️ {texts[1]}")
#     home_key = KeyboardButton(f"🏠 {texts[0]}")
#     keyboard.add(back_key, home_key)  
#     keyboard.resize_keyboard = True
#     return keyboard


# async def subcategory_keyboard(lang, cat_id):
#     texts = []
#     categories = SubCategory.objects.filter(category_id=cat_id).all()
#     texts = []
#     size = len(categories)
#     keyboard = ReplyKeyboardMarkup()
#     for i in categories:
#         if lang == "uz":
#             texts = ["Asosiy menyu", "Orqaga"]
#             keyboard.add(KeyboardButton(text=f"{i.name_uz}"))
#         elif lang == "en":
#             texts = ["Main menu", "Back"]
#             keyboard.add(KeyboardButton(text=f"{i.name_en}"))
#         elif lang == "tr":
#             texts = ["Главное меню", "Назад"]
#             keyboard.add(KeyboardButton(text=f"{i.name_ru}"))
#     back_key = KeyboardButton(f"⬅️ {texts[1]}")
#     home_key = KeyboardButton(f"🏠 {texts[0]}")
#     keyboard.add(back_key, home_key)  
#     keyboard.resize_keyboard = True
#     return keyboard



# async def product_keyboard(user_id, lang, sub_id):
#     texts = []
#     categories = Product.objects.filter(sub_category_id=sub_id).all()
#     texts = []
#     size = len(categories)
#     keyboard = ReplyKeyboardMarkup()
#     for i in categories:
#         if lang == "uz":
#             texts = ["Asosiy menyu", "Orqaga", "Savat"]
#             keyboard.add(KeyboardButton(text=f"{i.name_uz}"))
#         elif lang == "en":
#             texts = ["Main menu", "Back", "Корзина"]
#             keyboard.add(KeyboardButton(text=f"{i.name_en}"))
#         elif lang == "tr":
#             texts = ["Главное меню", "Назад", "Cart"]
#             keyboard.add(KeyboardButton(text=f"{i.name_ru}"))
#     cart_key = KeyboardButton(text=f"📥  {texts[2]}")
#     cart_test = await check_cart(user_id)
#     if cart_test:   
#         keyboard.add(cart_key)  
#     back_key = KeyboardButton(f"⬅️ {texts[1]}")
#     home_key = KeyboardButton(f"🏠 {texts[0]}")
#     keyboard.add(back_key, home_key)  
#     keyboard.resize_keyboard = True
#     return keyboard


async def cart_keyboard( user_id):
    texts = []
    user = User.objects.filter(user_id=user_id).first()
    texts = []
    carts = CartObject.objects.filter(user=user, confirm=True).all()
    keyboard = ReplyKeyboardMarkup()
    for i in carts:
        texts = ["Главное меню", "Назад", "Очистить корзину", "Завершить заказ"]
        keyboard.add(KeyboardButton(text=f"❌ {i.product.name}"))
    back_key = KeyboardButton(f"⬅️ {texts[1]}")
    home_key = KeyboardButton(f"🏠 {texts[0]}")
    clear_key = KeyboardButton(f"🗑 {texts[2]}")
    order_key = KeyboardButton(f"🛒 {texts[3]}")
    keyboard.add(clear_key, order_key)  
    keyboard.add(back_key, home_key)  
    keyboard.resize_keyboard = True
    return keyboard


async def pay_method(lang):
    texts = []
    if lang == "uz":
        texts = ["Click", "Payme", "Naqd pul orqali" , "Orqaga"]
    elif lang == "en":
        texts = ["Click", "Payme", "Cash", "Back"]
    elif lang == "tr":
        texts = ["Click", "Payme", "Наличными", "Назад"]

    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"🔵 {texts[0]}")
    key2 = KeyboardButton(text=f"🟢 {texts[1]}")
    key3 = KeyboardButton(text=f"💴 {texts[2]}")
    key4 = KeyboardButton(text=f"⬅️ {texts[3]}")
    keyboard.add(key1, key2, key3)
    keyboard.add(key4)
    keyboard.resize_keyboard = True
    return keyboard


async def cancel_order():
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"❌ Отмена заказа")
    keyboard.add(key1)
    keyboard.resize_keyboard = True
    return keyboard

    
async def location_send(lang):
    text = []
    if lang == 'uz':
        text = ['Joylashuvni ulashish', 'Oldingi manzillar', "Orqaga"]
    elif lang == 'ru':
        text = ['Отправить местоположение', 'Предыдущие адреса', "Назад"]
    elif lang == 'en':
        text = ['Send location', 'Previous addresses', "Back"]
    mrk = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    # bt = KeyboardButton(f'📍 {text[0]}', request_location=True)
    back_key = KeyboardButton(f"⬅️ {text[2]}")
    btn = KeyboardButton(f'🔂 {text[1]}')
    mrk.add(btn)
    mrk.add(back_key)
    return mrk


async def product_back_keyboard(lang):      
    texts = []
    keyboard = ReplyKeyboardMarkup()
    if lang == "uz":
        texts = ["Asosiy menyu", "Orqaga"]
    elif lang == "en":
        texts = ["Main menu", "Back"]
    elif lang == "tr":
        texts = ["Главное меню", "Назад"]
    back_key = KeyboardButton(f"⬅️ {texts[1]}")
    home_key = KeyboardButton(f"🏠 {texts[0]}")
    keyboard.add(back_key, home_key)  
    keyboard.resize_keyboard = True
    return keyboard


async def confirm_address(lang):
    text = []
    if lang == 'uz':
        text = ['Tasdiqlash', 'Qayta jo\'natish', 'Orqaga']
    elif lang == 'ru':
        text = ['Подтвердить', 'Отправить повторно', 'Назад']
    elif lang == 'en':
        text = ['Confirm', 'Send again', 'Back']
    markup =     keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"✅ {text[0]}")
    key2 = KeyboardButton(f"🔄 {text[1]}")
    keyboard.add(key1, key2)  
    keyboard.resize_keyboard = True
    return markup


async def location_keys(user_id, lang):
    locs = await get_address(user_id)
    keyboard = ReplyKeyboardMarkup()
    for i in locs:
        if lang == "uz":
            keyboard.add(KeyboardButton(text=f"{i.name}"))
        elif lang == "en":
            keyboard.add(KeyboardButton(text=f"{i.name}"))
        elif lang == "ru":
            keyboard.add(KeyboardButton(text=f"{i.name}"))
    back_key = KeyboardButton(f"⬅️ Назад")
    keyboard.add(back_key)  
    keyboard.resize_keyboard = True
    return keyboard


async def order_confirmation(lang):
    texts = []
    if lang == "uz":
        texts = ["Buyurtmani tasdiqlash", "Bekor qilish"]
    elif lang == "en":
        texts = ["Confirm order", "Cancel"]
    elif lang == "tr":
        texts = ["Подтвердить заказ", "Отмена"]

    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"✅ {texts[0]}")
    key2 = KeyboardButton(text=f"❌ {texts[1]}")
    keyboard.add(key1, key2)
    keyboard.resize_keyboard = True
    return keyboard


async def order_confirmation(lang):
    texts = []
    if lang == "uz":
        texts = ["Buyurtmani tasdiqlash", "Bekor qilish"]
    elif lang == "en":
        texts = ["Confirm order", "Cancel"]
    elif lang == "ru":
        texts = ["Подтвердить заказ", "Отмена"]

    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"✅ {texts[0]}")
    key2 = KeyboardButton(text=f"❌ {texts[1]}")
    keyboard.add(key1, key2)
    keyboard.resize_keyboard = True
    return keyboard


async def confirmation_keyboard(lang):
    texts = []
    if lang == "uz":
        texts = ["Tasdiqlash", "Bekor qilish"]
    elif lang == "en":
        texts = ["Confirm", "Cancel"]
    elif lang == "tr":
        texts = ["Подтвердить", "Отмена"]

    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"✅ {texts[0]}")
    key2 = KeyboardButton(text=f"❌ {texts[1]}")
    keyboard.add(key1, key2)
    keyboard.resize_keyboard = True
    return keyboard


async def filial_keyboard(lang):
    texts = []
    filials = Filial.objects.all()
    keyboard = ReplyKeyboardMarkup()
    for i in filials:
        if lang == "uz":
            texts = ["Asosiy menyu", "Orqaga"]
            keyboard.add(KeyboardButton(text=f"{i.filial_uz}"))
        elif lang == "en":
            texts = ["Main menu", "Back"]
            keyboard.add(KeyboardButton(text=f"{i.filial_en}"))
        elif lang == "tr":
            texts = ["Главное меню", "Назад"]
            keyboard.add(KeyboardButton(text=f"{i.filial_tr}"))
    back_key = KeyboardButton(f"⬅️ {texts[1]}")
    home_key = KeyboardButton(f"🏠 {texts[0]}")
    keyboard.add(back_key, home_key)  
    keyboard.resize_keyboard = True
    return keyboard



# async def confirm_keyboard():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="❌ Yo'q", callback_data=f"cancel"),
#                 InlineKeyboardButton(text="✅ Ha", callback_data=f"confirm"),
#             ],
#         ]
#     )
#     return markup


# async def get_or_back():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back"),
#                 InlineKeyboardButton(text="📑 Excell hujjatni yuklash", callback_data=f"get"),
#             ],
#         ]
#     )
#     return markup


# async def back_to():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_to_menu"),
#             ],
#         ]
#     )
#     return markup


# async def year_keyboard(years):
#     inline_keyboard = []
#     for i in years:
#         inline_keyboard.append([InlineKeyboardButton(text=f"{i}", callback_data=i)])
#     inline_keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_menu")])
#     markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
#     return markup


# Moths = {1: 'Yanvar', 2: 'Fevral', 3: 'Mart', 4: 'Aprel', 5: 'May', 6: 'Iyun', 7: 'Iyul', 8: 'Avgust', 9: 'Sentabr',
#          10: 'Oktyabr', 11: 'Noyabr', 12: 'Dekabr', }


# async def month_keyboard(date):
#     inline_keyboard = []
#     for i in date:
#         inline_keyboard.append([InlineKeyboardButton(text=f"{Moths[i]}", callback_data=i)])
#     inline_keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_menu")])
#     markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
#     return markup
