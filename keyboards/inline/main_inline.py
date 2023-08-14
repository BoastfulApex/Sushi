from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from backend.models import *
from utils.db_api.database import *


# async def language_keyboard():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#             InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="uz"),
#             InlineKeyboardButton(text="🇺🇸 English", callback_data="en"),
#             InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="ru")
#             ]
#             ])
#     return markup


async def confirm_payment(order_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"❌ Отмена", callback_data=f"cancel---{order_id}")],
            [InlineKeyboardButton(text=f"✅ Подтверждение оплаты", callback_data=f"confirm---{order_id}")],
        ]
    )
    return markup

async def delivered(order_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"✅ Подтверждение оплаты", callback_data=f"delivered_confirm---{order_id}")],
        ]
    )
    return markup


async def time_keyboard(order_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"10", callback_data=f"order_time-{order_id}-10"),
            InlineKeyboardButton(text=f"20", callback_data=f"order_time-{order_id}-20"),
            InlineKeyboardButton(text=f"30", callback_data=f"order_time-{order_id}-30"),
            InlineKeyboardButton(text=f"40", callback_data=f"order_time-{order_id}-40")]
        ]
    )
    return markup


async def rate_keyboard(order_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"1⭐️", callback_data=f"order_rate-{order_id}-1"),
                InlineKeyboardButton(text=f"2⭐️", callback_data=f"order_rate-{order_id}-2"),
                InlineKeyboardButton(text=f"3⭐️", callback_data=f"order_rate-{order_id}-3")
                ],
            [
                InlineKeyboardButton(text=f"4⭐️", callback_data=f"order_rate-{order_id}-4"),
                InlineKeyboardButton(text=f"5⭐️", callback_data=f"order_rate-{order_id}-5")
                ],
            [
                InlineKeyboardButton(text=f"Оставить без оценки", callback_data=f"order_rate-{order_id}-no_order")
                ]   
        ]
    )
    return markup


# async def back_keyboard(lang):
#     texts = []
#     if lang == "uz":
#         texts = ["Orqaga"]
#     elif lang == "en":
#         texts = ["Back"]
#     elif lang == "ru":
#         texts = ["Назад"]
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text=f"⬅️ {texts[0]}", callback_data="back")],
#         ]
#     )
#     return markup


async def about_menu(lang):
    texts = []
    if lang == "uz":
        texts = ["Telegram", "Facebook", "Youtube", "Instagram", "Orqaga"]
    elif lang == "en":
        texts = ["Telegram", "Facebook", "Youtube", "Instagram", "Back"]
    elif lang == "ru":
        texts = ["Телеграм", "Facebook", "Youtube", "Instagram", "Назад"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{texts[0]}", url="http://t.me/DunyaBunya")],
            [InlineKeyboardButton(text=f"{texts[1]}", url="https://www.facebook.com/dunyabunya.uz")],
            [InlineKeyboardButton(text=f"{texts[2]}", url="https://youtube.com/")],
            [InlineKeyboardButton(text=f" {texts[3]}", url="https://instagram.com/")],
        ]
    )
    return markup


async def go_search(lang):
    texts = []
    if lang == "uz":
        texts = ["Izlash"]
    elif lang == "en":
        texts = ["Search"]
    elif lang == "ru":
        texts = ["Поиск"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🔎 {texts[0]}", switch_inline_query_current_chat=""),
            ],
        ]
    )
    return markup


async def go_order():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🛍 Начать покупки ↗️", callback_data="go_shopping")],
        ]
    )
    return markup


async def category_keyboard(user_id):
    carts = await get_carts(user_id)        
    categories = Category.objects.all()
    markup = InlineKeyboardMarkup(row_width=2)
    if carts != '⚠️ Ваша корзина пуста':
        markup.add(InlineKeyboardButton(text=f"🛒 Корзина", callback_data="go_cart"))
    for i in categories:
        markup.insert(InlineKeyboardButton(text=f"{i.name}", callback_data=i.id))
    markup.add(InlineKeyboardButton(text=f"🔙 Назад", callback_data=f"back"))
    return markup


async def product_keyboard(cat_id):
    products = Product.objects.filter(category__id=cat_id, stop_list=False).all()
    markup = InlineKeyboardMarkup(row_width=2)
    for i in products:
        markup.insert(InlineKeyboardButton(text=f"{i.name}", callback_data=i.id))
    markup.add(InlineKeyboardButton(text=f"🔙 Назад", callback_data=f"back"))
    return markup


async def order_keyboard(lang, cart_id):
    texts = []
    if lang == "uz":
        texts = ["Savatchaga qo'shish", "Orqaga"]
    elif lang == "en":
        texts = ["Add to card", "Back"]
    elif lang == "ru":
        texts = ["Добавить в корзину", "Назад"]

    markup = InlineKeyboardMarkup(row_width=3)
    cart = CartObject.objects.filter(id=cart_id).first()
    markup.insert(
        InlineKeyboardButton(text=f"➖", callback_data=f"cart_minus-{cart.id}"))
    markup.insert(
        InlineKeyboardButton(text=f"{cart.count}", callback_data="no_call-1"))
    markup.insert(
        InlineKeyboardButton(text=f"➕", callback_data=f"cart_plus-{cart.id}"))
    markup.row(InlineKeyboardButton(text=f"📥 {texts[0]} ", callback_data=f"confirm-{cart.id}"))
    markup.row(InlineKeyboardButton(text="⬅️ Назад ", callback_data=f"cancel-{cart.id}"))
    return markup


async def product_count_keyboard(lang, cart_id):
    texts = []
    if lang == "uz":
        texts = ["Savatchaga qo'shish", "Orqaga"]
    elif lang == "en":
        texts = ["Add to card", "Back"]
    elif lang == "ru":
        texts = ["Добавить в корзину", "Назад"]

    markup = InlineKeyboardMarkup(row_width=3)
    cart = CartObject.objects.filter(id=cart_id).first()
    markup.insert(
        InlineKeyboardButton(text=f"➖", callback_data=f"cart_minus-{cart.id}"))
    markup.insert(
        InlineKeyboardButton(text=f"{cart.count}", callback_data="no_call-1"))
    markup.insert(
        InlineKeyboardButton(text=f"➕", callback_data=f"cart_plus-{cart.id}"))
    markup.row(InlineKeyboardButton(text=f"📥 {texts[0]} ", callback_data=f"confirm-{cart.id}"))
    markup.row(InlineKeyboardButton(text="⬅️ Back ", callback_data=f"cancel-{cart.id}"))
    return markup



# async def back_admin_menu():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_admin"),
#             ],
#         ]
#     )
#     return markup


# async def doctor_in_admin():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="🗓 Bugungi kungi keshbekni ko'rish", callback_data="kash_today")],
#             [InlineKeyboardButton(text="📅 Alohida kun uchun keshbekni ko'rish", callback_data="kash_day")],
#             [InlineKeyboardButton(text="📆 Shu oy uchun keshbekni ko'rish", callback_data="kash_this_month")],
#             [InlineKeyboardButton(text="🗒 Alohida oy uchun keshbekni ko'rish", callback_data="kash_month")],
#             [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_admin")],
#         ]
#     )
#     return markup


# async def back_keyboard():
#     keyboard = ReplyKeyboardMarkup()
#     key1 = KeyboardButton(text="⬅️ Bekor qilish")
#     keyboard.add(key1)
#     keyboard.resize_keyboard = True
#     return keyboard


# async def ask_keyboard():
#     keyboard = ReplyKeyboardMarkup()
#     key1 = KeyboardButton(text="💵 Avans so'rash")
#     keyboard.add(key1)
#     keyboard.resize_keyboard = True
#     return keyboard


# async def admin_menu():
#     keyboard = ReplyKeyboardMarkup(row_width=2)
#     key1 = KeyboardButton(text="Eslatma qo'shish")
#     keyboard.add(key1)
#     keyboard.resize_keyboard = True
#     return keyboard

# async def client_keys():
#     keyboard = ReplyKeyboardMarkup(row_width=2)
#     key1 = KeyboardButton(text="Keyingi to'lovni ko'rish")
#     keyboard.add(key1)
#     keyboard.resize_keyboard = True
#     return keyboard
