import os, requests, subprocess, json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

STORY_PROMPT = """
Write an 8-minute cartoon story in Hinglish for kids.
Theme: Adventure + Moral
Characters: A smart boy named Raju and a cute robot named Bolt.
Tone: Fun, simple, emotional.
End with a cliffhanger for next episode.
Also divide the story into 8 scenes with short scene descriptions.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Cartoon Bot Ready!\nType /new_episode to generate cartoon.")

async def new_episode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Generating story...")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": STORY_PROMPT}]
    }

    r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                      headers=headers, json=data)

    story = r.json()["choices"][0]["message"]["content"]
    open("story.txt", "w", encoding="utf-8").write(story)

    await update.message.reply_text("✅ Story generated!\n(Next: images + voice + video in next steps)")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new_episode", new_episode))
    app.run_polling()

if __name__ == "__main__":
    main()
