import os
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
# تنظیمات اصلی ربات
# =========================

# توکن جدید رباتت را اینجا بگذار
TOKEN = "8698498177:AAFvlzO6uPySexnY8EWR976MRbGlUfPG7_U"


# اول بگذار 0 بماند
# بعد داخل ربات دستور /myid را بزن
# عددی که ربات داد را اینجا جایگزین کن
ADMIN_ID = 1633238816

# آیدی پشتیبانی بدون @
SUPPORT_USERNAME = "mahdi_rzqhi"

# شماره کارت و نام صاحب کارت
CARD_NUMBER = "6219861402793177"
CARD_OWNER = "مهدی رزاقی"


# =========================
# محصولات / پلن‌ها
# =========================

PRODUCTS = {
    "plan_1gb": {
        "title": "اشتراک ۱ گیگابایت",
        "price": "۲۳,۰۰۰ تومان",
        "duration": "۳۰ روز",
        "delivery_text": "✅ اطلاعات اشتراک دیجیتال شما اینجا قرار می‌گیرد."
    },
    "plan_3gb": {
        "title": "اشتراک ۳ گیگابایت",
        "price": "۶۷,۰۰۰ تومان",
        "duration": "۳۰ روز",
        "delivery_text": "✅ اطلاعات اشتراک دیجیتال شما اینجا قرار می‌گیرد."
    },
    "plan_5gb": {
        "title": "اشتراک ۵ گیگابایت",
        "price": "۱۱۵,۰۰۰ تومان",
        "duration": "۳۰ روز",
        "delivery_text": "✅ اطلاعات اشتراک دیجیتال شما اینجا قرار می‌گیرد."
    },
}

# سفارش‌های کاربران تا وقتی ربات روشن است اینجا ذخیره می‌شود
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
        [InlineKeyboardButton("🟢 اشتراک ۱ گیگابایت - 23,000 تومان", callback_data="buy_plan_1gb")],
        [InlineKeyboardButton("🟢 اشتراک ۳ گیگابایت - 67,000 تومان", callback_data="buy_plan_3gb")],
        [InlineKeyboardButton("🟢 اشتراک ۵ گیگابایت - 150,000 تومان", callback_data="buy_plan_5gb")],
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
        f"این عدد را داخل کد، جای ADMIN_ID قرار بده.",
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
💰 قیمت: ۲۳,۰۰۰ تومان
⏳ اعتبار: ۳۰ روز

🟢 اشتراک ۳ گیگابایت
💰 قیمت: ۶۷,۰۰۰ تومان
⏳ اعتبار: ۳۰ روز

🟢 اشتراک ۵ گیگابایت
💰 قیمت: 150,000 تومان
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
            "⚠️ هنوز ADMIN_ID داخل کد تنظیم نشده است.\n"
            "داخل ربات دستور /myid را بزن، عدد را بردار و داخل کد جای ADMIN_ID = 0 بگذار."
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
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    run_bot()