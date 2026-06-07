import asyncio
import random
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from hydrogram import Client, filters
from hydrogram.enums import ChatMemberStatus, ChatType

# --- EVENT LOOP FIX FOR PYTHON 3.14 (SABSE PEHLE RUN HOGA) ---
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# ---------------- CONFIGURATION ----------------
API_ID = 38977169  
API_HASH = "39780ae25693b15b64648591faba91b3"
BOT_TOKEN = "8657791317:AAF19fslbsdXm9R8pD7tq8m0vzzDBirEipg"
OWNER_ID = 8619340682  
# -----------------------------------------------

# Ab app initialize bina kisi error ke safely ho jayega
app = Client("spyyt_coinflip_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
next_prediction = None

# --- DUMMY WEB SERVER FOR RENDER PORT TIMEOUT ---
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is Live!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(("0.0.0.0", port), DummyServer)
        print(f"🌍 Web Server successfully started on port {port}")
        server.serve_forever()
    except Exception as e:
        print(f"⚠️ Port {port} busy tha, trying backup port 8080...")
        try:
            server = HTTPServer(("0.0.0.0", 8080), DummyServer)
            server.serve_forever()
        except Exception as err:
            print(f"❌ Server error: {err}")

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
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                is_admin = True
        except Exception as e:
            print(f"Admin check error: {e}")
    else:
        is_admin = True

    if not is_admin:
        funny_roasts = [
            "Tu pehle admin ban ke aa! 😂",
            "Tere haath mein coin nahi, katora accha lagega! 😜",
            "VIP Access Only! Aam janta ke liye flip allowed nahi hai. 🤌",
            "Chup chap baith ja, sirf Admins ka raj chalta hai yahan! 👑"
        ]
        await message.reply_text(random.choice(funny_roasts))
        return

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

async def start_bot():
    print("🔥 SPYYT ESCROW FLIP BOT STARTED VIA HYDROGRAM 🔥")
    threading.Thread(target=run_web_server, daemon=True).start()
    await app.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop.run_until_complete(start_bot())
      
