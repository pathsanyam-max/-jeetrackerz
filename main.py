import telebot
import json
import os

TOKEN = "8232273708:AAHzvfCaEebwp0k9NDoRof93uKJnXWWHrsI"
ADMIN_ID = 7371121826

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"

# Load data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {"books": {}, "users": []}

def save():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if user_id not in data["users"]:
        data["users"].append(user_id)
        save()

    bot.send_message(
        message.chat.id,
        "══════════════════════════════\n"
        "        🎓  𝐉𝐄𝐄 𝐓𝐑𝐀𝐂𝐊𝐄𝐑 𝐕𝐀𝐔𝐋𝐓  🎓\n"
        "══════════════════════════════\n\n"
        "📘 Official Academic Resource Portal\n\n"
        "Secure access for serious aspirants.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ Instant PDF Delivery\n"
        "🔐 Unique Link System\n"
        "📂 Organized Digital Library\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📢 Backup Channel:\n"
        "https://t.me/JEECBSENEETBOOKS\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )

# ---------------- ADD BOOK ----------------
@bot.message_handler(content_types=['document'])
def save_book(message):
    if message.from_user.id != ADMIN_ID:
        return

    if not message.caption:
        bot.reply_to(message, "⚠ Book name caption me likho.")
        return

    key = message.caption
    file_id = message.document.file_id

    data["books"][key] = file_id
    save()

    bot_username = bot.get_me().username
    link = f"https://t.me/{bot_username}?start={key}"

    bot.reply_to(
        message,
        f"✅ Book Saved!\n\n🔗 Unique Link:\n{link}"
    )

# ---------------- STATS ----------------
@bot.message_handler(commands=['stats'])
def stats(message):
    if message.from_user.id != ADMIN_ID:
        return

    bot.reply_to(
        message,
        f"👥 Total Users: {len(data['users'])}\n"
        f"📚 Total Books: {len(data['books'])}"
    )

# ---------------- RUN ----------------
print("Bot Running...")
bot.infinity_polling()
