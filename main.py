import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is Live!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), DummyServer)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

# --- ISKE NICHE AAPKA PURANA PYROGRAM CODE CHALTA RAHEGA ---

from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
import asyncio
import random

# ---------------- CONFIGURATION ----------------
API_ID = 38977169  # Apna API ID dalein
API_HASH = "39780ae25693b15b64648591faba91b3"
BOT_TOKEN = "8657791317:AAGlhOcsX40COqVO84q2f7agAZWySpH-i_o"
OWNER_ID = 8619340682  # Apni real Telegram Numeric ID dalein
# -----------------------------------------------

app = Client("spyyt_coinflip_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

next_prediction = None

# 1. SECRET CHEATING COMMAND
@app.on_message(filters.command("predict") & filters.user(OWNER_ID))
async def set_prediction(client, message):
    global next_prediction
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply_text("❌ Usage: /predict heads ya /predict tails\n/predict clear reset karne ke liye.")
            return

        choice = parts[1].lower()
        if choice in ["heads", "head"]:
            next_prediction = "HEADS"
            await message.reply_text("😈 The God Mode: Agla result HEADS aayega!")
        elif choice in ["tails", "tail"]:
            next_prediction = "TAILS"
            await message.reply_text("😈 The God Mode: Agla result TAILS aayega!")
        elif choice == "clear":
            next_prediction = None
            await message.reply_text("✅ Prediction cleared! Normal random mode on.")
        else:
            await message.reply_text("❌ Galat choice! Sirf heads ya tails likhein.")

    except Exception as e:
        print(f"Predict Error: {e}")

# 2. MAIN GAME TRIGGER
@app.on_message(filters.text & filters.regex(r"(?i)^\s*flip\s*$"))
async def handle_flip(client, message):
    global next_prediction

    is_admin = False
    # ERROR YAHAN THA: Ab filters.ChatType ki jagah sirf ChatType hai
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                is_admin = True
        except Exception as e:
            print(f"Admin check error: {e}")
    else:
        is_admin = True

    # ---- NORMAL MEMBER (TROLL MODE) ----
    if not is_admin:
        funny_roasts = [
            "Tu pehle admin ban ke aa! 😂",
            "Tere haath mein coin nahi, katora accha lagega! 😜",
            "VIP Access Only! Aam janta ke liye flip allowed nahi hai. 🤌",
            "Chup chap baith ja, sirf Admins ka raj chalta hai yahan! 👑"
        ]
        await message.reply_text(random.choice(funny_roasts))
        return

    # ---- ADMIN/OWNER (REAL ACTION) ----
    frame1 = (
        "╔════════════════════╗\n"
        "      SPYYT ESCROW \n"
        "╚════════════════════╝\n\n"
        "⚡ RNG CORE ONLINE\n"
        "🪙 COIN LAUNCHED 🚀\n"
        "🎲 SPINNING... [|]\n\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "⏳ Waiting for result..."
    )

    msg = await message.reply_text(frame1)
    await asyncio.sleep(1)

    frame2 = (
        "╔════════════════════╗\n"
        "      SPYYT ESCROW \n"
        "╚════════════════════╝\n\n"
        "⚡ RNG CORE ONLINE\n"
        "🪙 COIN LAUNCHED \n"
        "🎲 ANALYZING RESULT... [/]\n\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "⏳ Calculating outcome..."
    )
    await msg.edit_text(frame2)
    await asyncio.sleep(1.2)

    if next_prediction is not None:
        final_result = next_prediction
        next_prediction = None
    else:
        final_result = random.choice(["HEADS", "TAILS"])

    final_card = (
        "╔════════════════════╗\n"
        "      SPYYT ESCROW \n"
        "╚════════════════════╝\n\n"
        "⚡ RNG CORE ONLINE\n"
        "🪙 COIN LAUNCHED \n"
        "🎲 ANALYZING RESULT \n\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🏆 FINAL OUTCOME\n\n"
        f"        🪙 **{final_result}** 🪙\n\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    await msg.edit_text(final_card)


import asyncio

async def main():
    print("🔥 SPYYT ESCROW FLIP BOT STARTED 🔥")
    await app.start()
    # Bot ko background me chalte rehne ke liye loop
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
