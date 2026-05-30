import os
import threading

from flask import Flask

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# Web server for Render
# =========================

web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Bot is running!"


def run_web_server():
    port = int(os.getenv("PORT", "10000"))
    web_app.run(host="0.0.0.0", port=port)


# =========================
# تنظیمات اصلی ربات
# =========================

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

SUPPORT_USERNAME = "mahdi_rzqhi"

CARD_NUMBER = "6219861402793177"
CARD_OWNER = "مهدی رزقی"


# =========================
# محصولات / پلن‌ها
# =========================

PRODUCTS = {
    "plan_1gb": {
        "title": "اشتراک ۱ گیگابایت",
        "price": "۲۵,۰۰۰ تومان",
        "duration": "۳۰ روز",
        "delivery_text": "✅ اطلاعات اشتراک دیجیتال شما اینجا قرار می‌گیرد."
    },
    "plan_3gb": {
        "title": "اشتراک ۳ گیگابایت",
        "price": "۷۵,۰۰۰ تومان",
        "duration": "۳۰ روز",
        "delivery_text": "✅ اطلاعات اشتراک دیجیتال شما اینجا قرار می‌گیرد."
    },
    "plan_5gb": {
        "title": "اشتراک ۵ گیگابایت",
        "price": "۱۲۵,۰۰۰ تومان",
        "duration": "۳۰ روز",
        "delivery_text": "✅ اطلاعات اشتراک دیجیتال شما اینجا قرار می‌گیرد."
    },
}

user_orders = {}


# =========================
# منوها
# =========================

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🛒 مشاهده محصولات", callback_data="products")],
        [InlineKeyboardButton("💳 خرید", callback_data="buy")],
        [InlineKeyboardButton("📤 راهنمای ارسال رسید", callback_data="receipt_help")],
        [InlineKeyboardButton("🎧 پشتیبانی", callback_data="support")],
    ]
    return InlineKeyboardMarkup(keyboard)


def buy_menu():
    keyboard = [
        [InlineKeyboardButton("🟢 اشتراک ۱ گیگابایت - ۲۵,۰۰۰ تومان", callback_data="buy_plan_1gb")],
        [InlineKeyboardButton("🟢 اشتراک ۳ گیگابایت - ۷۵,۰۰۰ تومان", callback_data="buy_plan_3gb")],
        [InlineKeyboardButton("🟢 اشتراک ۵ گیگابایت - ۱۲۵,۰۰۰ تومان", callback_data="buy_plan_5gb")],
        [InlineKeyboardButton("🔙 برگشت به منو", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)


# =========================
# دستورها
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
سلام 👋
به ربات فروشگاه دیجیتال خوش آمدید.

لطفاً یکی از گزینه‌های زیر را انتخاب کنید:
"""
    await update.message.reply_text(text, reply_markup=main_menu())


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        f"آیدی عددی شما:\n`{user_id}`\n\n"
        f"این عدد باید در Render داخل Environment Variable با نام ADMIN_ID قرار بگیرد.",
        parse_mode="Markdown"
    )


# =========================
# مدیریت دکمه‌ها
# =========================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "products":
        text = """
📦 محصولات موجود

🟢 اشتراک ۱ گیگابایت
💰 قیمت: 25,000 تومان
⏳ اعتبار: ۳۰ روز

🟢 اشتراک ۳ گیگابایت
💰 قیمت: 75,000 تومان
⏳ اعتبار: ۳۰ روز

🟢 اشتراک ۵ گیگابایت
💰 قیمت: 100,000 تومان
⏳ اعتبار: ۳۰ روز

📩 تحویل پس از تأیید پرداخت توسط ادمین

برای ثبت سفارش روی گزینه خرید بزنید.
"""
        await query.edit_message_text(text, reply_markup=main_menu())

    elif data == "buy":
        await query.edit_message_text(
            "لطفاً پلن مورد نظر را انتخاب کنید:",
            reply_markup=buy_menu()
        )

    elif data in ["buy_plan_1gb", "buy_plan_3gb", "buy_plan_5gb"]:
        user = query.from_user

        if data == "buy_plan_1gb":
            plan_key = "plan_1gb"
        elif data == "buy_plan_3gb":
            plan_key = "plan_3gb"
        else:
            plan_key = "plan_5gb"

        user_orders[user.id] = plan_key
        product = PRODUCTS[plan_key]

        text = f"""
✅ سفارش شما ثبت شد.

📦 پلن انتخابی: {product['title']}
💰 مبلغ: {product['price']}
⏳ اعتبار: {product['duration']}

لطفاً مبلغ را به شماره کارت زیر واریز کنید:

`{CARD_NUMBER}`

به نام:
`{CARD_OWNER}`

بعد از پرداخت، تصویر رسید را همین‌جا داخل ربات ارسال کنید.
"""
        await query.edit_message_text(text, parse_mode="Markdown")

    elif data == "receipt_help":
        text = """
📤 راهنمای ارسال رسید

۱. ابتدا از بخش «خرید» یک پلن انتخاب کنید.
۲. مبلغ پلن را واریز کنید.
۳. عکس رسید پرداخت را همین‌جا داخل ربات ارسال کنید.
۴. بعد از بررسی ادمین، سفارش شما تأیید یا رد می‌شود.
"""
        await query.edit_message_text(text, reply_markup=main_menu())

    elif data == "support":
        text = f"""
🎧 پشتیبانی

برای ارتباط با پشتیبانی به آیدی زیر پیام بدهید:

@{SUPPORT_USERNAME}
"""
        await query.edit_message_text(text, reply_markup=main_menu())

    elif data == "back":
        await query.edit_message_text("منوی اصلی:", reply_markup=main_menu())

    elif data.startswith("approve_"):
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("⛔ شما دسترسی ادمین ندارید.")
            return

        user_id = int(data.replace("approve_", ""))
        plan_key = user_orders.get(user_id)

        if not plan_key:
            await query.edit_message_text("❌ سفارش این کاربر پیدا نشد.")
            return

        product = PRODUCTS[plan_key]

        await context.bot.send_message(
            chat_id=user_id,
            text=f"""
✅ سفارش شما تأیید شد.

📦 پلن: {product['title']}
⏳ اعتبار: {product['duration']}

{product['delivery_text']}
"""
        )

        await query.edit_message_text("✅ سفارش تأیید شد و پیام تحویل برای کاربر ارسال شد.")

    elif data.startswith("reject_"):
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("⛔ شما دسترسی ادمین ندارید.")
            return

        user_id = int(data.replace("reject_", ""))

        await context.bot.send_message(
            chat_id=user_id,
            text=f"""
❌ رسید پرداخت شما تأیید نشد.

لطفاً برای بررسی بیشتر با پشتیبانی ارتباط بگیرید:
@{SUPPORT_USERNAME}
"""
        )

        await query.edit_message_text("❌ سفارش رد شد و پیام برای کاربر ارسال شد.")


# =========================
# دریافت رسید پرداخت
# =========================

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    plan_key = user_orders.get(user_id)

    if not plan_key:
        await update.message.reply_text(
            "لطفاً ابتدا از بخش خرید، یک پلن انتخاب کنید و بعد رسید را ارسال کنید.",
            reply_markup=main_menu()
        )
        return

    product = PRODUCTS[plan_key]

    await update.message.reply_text("✅ رسید شما دریافت شد و برای ادمین ارسال گردید.")

    if ADMIN_ID == 0:
        await update.message.reply_text(
            "⚠️ هنوز ADMIN_ID تنظیم نشده است.\n"
            "داخل ربات دستور /myid را بزن، عدد را بردار و در Render داخل Environment Variable با نام ADMIN_ID قرار بده."
        )
        return

    caption = f"""
📥 سفارش جدید

👤 کاربر: {user.full_name}
🆔 آیدی عددی: {user_id}
📦 پلن: {product['title']}
💰 مبلغ: {product['price']}
⏳ اعتبار: {product['duration']}

لطفاً رسید را بررسی کنید.
"""

    keyboard = [
        [
            InlineKeyboardButton("✅ تأیید سفارش", callback_data=f"approve_{user_id}"),
            InlineKeyboardButton("❌ رد سفارش", callback_data=f"reject_{user_id}")
        ]
    ]

    photo_id = update.message.photo[-1].file_id

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_id,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# پیام‌های متنی معمولی
# =========================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "پیام شما دریافت شد.\nبرای شروع از /start استفاده کنید.",
        reply_markup=main_menu()
    )


# =========================
# اجرای ربات
# =========================

def run_bot():
    if not TOKEN:
        raise ValueError("BOT_TOKEN تنظیم نشده است. لطفاً BOT_TOKEN را در Render Environment Variables قرار بده.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()

    run_bot()
