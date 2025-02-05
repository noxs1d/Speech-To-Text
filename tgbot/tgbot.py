import os
import ffmpeg
import whisper
import torch
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, CallbackContext

TOKEN = "API-key"


model = whisper.load_model("base",torch.device("cuda" if torch.cuda.is_available() else "cpu"))

async def handle_audio(update: Update, context: CallbackContext):
    file = None

    if update.message.voice:
        file = await update.message.voice.get_file()
    elif update.message.audio:
        file = await update.message.audio.get_file()
    elif update.message.video_note:
        file = await update.message.video_note.get_file()
    elif update.message.document:
        file = await update.message.document.get_file()

    if file:
        file_path = f"downloads/{file.file_id}.ogg"
        wav_path = f"downloads/{file.file_id}.wav"


        await file.download_to_drive(file_path)


        ffmpeg.input(file_path).output(wav_path, format="wav").run(overwrite_output=True)


        result = model.transcribe(wav_path)
        text = result["text"] or "Распознать текст не удалось."


        await update.message.reply_text(f"Распознанный текст:\n\n{text}")

        os.remove(file_path)
        os.remove(wav_path)

# Команда /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Отправьте мне аудиофайл или голосовое сообщение, и я переведу его в текст.")

# Настройки бота
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.VIDEO_NOTE | filters.Document.ALL, handle_audio))

    print("🤖 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    main()
