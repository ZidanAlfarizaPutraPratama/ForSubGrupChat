import os
import logging
import gridfs
import aiohttp
from bson import ObjectId
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['video_db']
fs = gridfs.GridFS(db)

# Telegram bot token and information
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Get OWNER_IDS from environment variable
owner_ids_env = os.getenv("OWNER_ID", "")
OWNER_IDS = list(map(int, owner_ids_env.split(','))) if owner_ids_env else []

# Initialize verification link
verification_link = os.getenv("VERIFICATION_LINK")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Storage for verification status and requests
verification_status = {}
verification_requests = {}

# Function to set verification link
async def set_verification_link(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in OWNER_IDS:
        await update.message.reply_text("Anda tidak memiliki izin untuk mengubah link verifikasi.")
        return

    if context.args:
        new_link = context.args[0]
        global verification_link
        verification_link = new_link
        await update.message.reply_text(f"Link verifikasi telah diperbarui menjadi: {verification_link}")
        logger.info(f"Link verifikasi diperbarui oleh pemilik: {verification_link}")
    else:
        await update.message.reply_text("Silakan berikan link baru setelah perintah, misalnya: /set_verification_link <link_baru>")

# Function to show help with buttons (only for owners)
async def help_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in OWNER_IDS:
        await update.message.reply_text("Anda tidak memiliki izin untuk melihat bantuan.")
        return

    keyboard = [
        [InlineKeyboardButton("Perintah", callback_data='show_commands')],
        [InlineKeyboardButton("Kembali", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=user_id, text="Berikut adalah opsi bantuan:", reply_markup=reply_markup)

# Function to display commands when the button is pressed
async def show_commands(update: Update, context: CallbackContext):
    commands_text = (
        "Berikut adalah daftar perintah yang dapat Anda gunakan:\n"
        "1. /start - Memulai interaksi dengan bot.\n"
        "2. /set_verification_link <link_baru> - Mengubah link verifikasi (hanya untuk pemilik).\n"
        "3. Lihat Video - Menampilkan daftar video yang tersedia.\n"
        "4. Verifikasi - Mengarahkan Anda ke link verifikasi.\n"
        "5. Konfirmasi Bergabung - Memungkinkan Anda mengirimkan screenshot untuk verifikasi.\n"
        "6. Upload Video - Mengizinkan pemilik untuk mengupload video.\n"
        "7. Hapus Video - Mengizinkan pemilik untuk menghapus video yang tersedia.\n"
    )
    await context.bot.send_message(chat_id=update.callback_query.from_user.id, text=commands_text)

# Function for the start command
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Lihat Video", callback_data='list_videos')],
        [InlineKeyboardButton("Verifikasi", url=verification_link)],
        [InlineKeyboardButton("Konfirmasi Bergabung", callback_data='confirm_join')],
    ]
    
    if update.message.from_user.id in OWNER_IDS:
        keyboard.append([InlineKeyboardButton("Upload Video", callback_data='upload_video')])
        keyboard.append([InlineKeyboardButton("Hapus Video", callback_data='delete_video')])  # New option
        keyboard.append([InlineKeyboardButton("Bantuan", callback_data='help')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Selamat datang! Silakan bergabung ke grup di bawah ini:\n"
        f"{verification_link}\n\n"
        "Setelah bergabung, silakan klik 'Konfirmasi Bergabung'.",
        reply_markup=reply_markup
    )

# Function to confirm joining
async def confirm_join(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    user_name = update.callback_query.from_user.username or "User Tanpa Username"
    
    if user_id in OWNER_IDS:
        await update.callback_query.answer("Anda adalah pemilik, tidak perlu konfirmasi.")
        verification_status[user_id] = True
        await context.bot.send_message(chat_id=user_id, text="Anda telah terverifikasi secara otomatis sebagai pemilik.")
        return

    verification_requests[user_id] = {"name": user_name, "screenshot": None}
    await update.callback_query.answer("Silakan kirim screenshot setelah bergabung.")
    await context.bot.send_message(chat_id=user_id, text="Silakan kirim screenshot sebagai bukti keanggotaan Anda.")

# Function to handle the screenshot sent by the user
async def handle_screenshot(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in verification_requests and verification_requests[user_id]["screenshot"] is None:
        photo_file = update.message.photo[-1]
        file_id = photo_file.file_id
        file = await context.bot.get_file(file_id)

        async with aiohttp.ClientSession() as session:
            async with session.get(file.file_path) as response:
                if response.status == 200:
                    photo_data = await response.read()
                    user_name = verification_requests[user_id]["name"]
                    for owner_id in OWNER_IDS:
                        await context.bot.send_photo(chat_id=owner_id, photo=photo_data)  # Send to all owners

                        keyboard = [
                            [InlineKeyboardButton("Approve", callback_data=f'acc_{user_id}')],
                            [InlineKeyboardButton("Reject", callback_data=f'reject_{user_id}')],
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)

                        await context.bot.send_message(chat_id=owner_id, text=f"User {user_name} ({user_id}) mengirimkan screenshot untuk verifikasi.", reply_markup=reply_markup)
                    verification_requests[user_id]["screenshot"] = "Screenshot received"
                    await update.message.reply_text("Screenshot telah diterima. Menunggu verifikasi dari pemilik bot.")
                else:
                    await update.message.reply_text("Terjadi kesalahan saat mengunduh screenshot.")
    else:
        await update.message.reply_text("Anda belum mengonfirmasi bergabung. Silakan gunakan tombol 'Konfirmasi Bergabung'.")

# Function to start video upload process
async def upload_video(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    if user_id not in OWNER_IDS:
        await update.callback_query.answer("Anda tidak memiliki izin untuk mengupload video.")
        return

    await update.callback_query.answer()
    await context.bot.send_message(chat_id=user_id, text="Silakan masukkan nama file untuk video (tanpa ekstensi):")
    context.user_data['uploading'] = True

# Function to handle video name input
async def handle_video_name(update: Update, context: CallbackContext):
    if context.user_data.get('uploading'):
        context.user_data['video_name'] = update.message.text
        await update.message.reply_text("Silakan kirim video Anda sekarang.")
    else:
        await update.message.reply_text("Silakan gunakan tombol 'Upload Video' untuk memulai proses upload.")

# Function to handle video upload
async def handle_video_upload(update: Update, context: CallbackContext):
    if context.user_data.get('uploading'):
        video_file = update.message.video
        if video_file is None:
            await update.message.reply_text("Tidak ada video yang ditemukan dalam pesan.")
            return

        file_id = video_file.file_id
        file = await context.bot.get_file(file_id)

        async with aiohttp.ClientSession() as session:
            async with session.get(file.file_path) as response:
                if response.status == 200:
                    video_data = await response.read()
                    
                    video_name = context.user_data.get('video_name', file_id)  # Use custom name or fallback to file ID
                    fs.put(video_data, filename=f"{video_name}.mp4")  # Save video with custom name

                    await update.message.reply_text("Video berhasil diupload!")
                    context.user_data['uploading'] = False
                    context.user_data.pop('video_name', None)  # Clear video name after upload
                else:
                    await update.message.reply_text("Terjadi kesalahan saat mengunduh video.")
    else:
        await update.message.reply_text("Silakan gunakan tombol 'Upload Video' untuk mengupload video.")

# Function to approve verification
async def approve_verification(update: Update, context: CallbackContext):
    user_id = int(update.callback_query.data.split('_')[1])
    if user_id in verification_requests and verification_requests[user_id]["screenshot"] is not None:
        verification_status[user_id] = True
        await update.callback_query.answer("Verifikasi Anda diterima.")
        await context.bot.send_message(chat_id=user_id, text="Verifikasi Anda diterima. Anda dapat melihat video sekarang.")
        logger.info(f"User {user_id} telah diverifikasi: ACC")
        del verification_requests[user_id]  # Remove request after approval
    else:
        await update.callback_query.answer("Tidak ada screenshot yang tersedia untuk verifikasi.")

# Function to reject verification
async def reject_verification(update: Update, context: CallbackContext):
    user_id = int(update.callback_query.data.split('_')[1])
    if user_id in verification_requests:
        del verification_requests[user_id]
        await update.callback_query.answer("Verifikasi Anda ditolak.")
        await context.bot.send_message(chat_id=user_id, text="Verifikasi Anda ditolak.")
        logger.info(f"User {user_id} telah ditolak verifikasinya: REJECT")
    else:
        await update.callback_query.answer("Tidak ada permintaan verifikasi yang ditemukan.")

# Function to display videos for deletion
async def delete_video(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    if user_id not in OWNER_IDS:
        await update.callback_query.answer("Anda tidak memiliki izin untuk menghapus video.")
        return

    keyboard = []
    for video in fs.find():
        keyboard.append([InlineKeyboardButton(video.filename, callback_data=f'delete_{video._id}')])

    if keyboard:
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=user_id, text="Pilih video untuk dihapus:", reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=user_id, text="Tidak ada video yang tersedia untuk dihapus.")

# Function to handle video deletion
async def remove_video(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    if user_id not in OWNER_IDS:
        await update.callback_query.answer("Anda tidak memiliki izin untuk menghapus video.")
        return

    video_id = update.callback_query.data.split('_')[1]  # Get the video ID from the callback data
    if not ObjectId.is_valid(video_id):
        await update.callback_query.answer("ID video tidak valid.")
        return

    # Remove video from GridFS
    fs.delete(ObjectId(video_id))
    await update.callback_query.answer("Video telah dihapus.")
    await context.bot.send_message(chat_id=user_id, text="Video berhasil dihapus.")

# Function to send video from GridFS
async def send_video(update: Update, context: CallbackContext):
    video_id = update.callback_query.data
    if not ObjectId.is_valid(video_id):
        await update.callback_query.answer("ID video tidak valid.")
        return

    try:
        video_file = fs.find_one({'_id': ObjectId(video_id)})
    except Exception as e:
        await update.callback_query.answer("Terjadi kesalahan saat mencari video.")
        logger.error(f"Error fetching video: {e}")
        return
    
    if video_file:
        video_data = video_file.read()
        await context.bot.send_video(chat_id=update.callback_query.from_user.id, video=video_data)
    else:
        await update.callback_query.answer("Video tidak ditemukan!")

# Function to display the list of videos
async def list_videos(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    if not verification_status.get(user_id, False):
        await context.bot.send_message(chat_id=user_id, text="Anda tidak dapat melihat video karena verifikasi Anda ditolak.")
        return

    keyboard = []
    for video in fs.find():
        keyboard.append([InlineKeyboardButton(video.filename, callback_data=str(video._id))])

    if keyboard:
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=user_id, text="Silakan pilih video untuk dilihat:", reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=user_id, text="Tidak ada video yang tersedia.")

# Main function
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("set_verification_link", set_verification_link))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(confirm_join, pattern='confirm_join'))
    application.add_handler(CallbackQueryHandler(approve_verification, pattern='acc_.*'))
    application.add_handler(CallbackQueryHandler(reject_verification, pattern='reject_.*'))
    application.add_handler(CallbackQueryHandler(upload_video, pattern='upload_video'))
    application.add_handler(CallbackQueryHandler(delete_video, pattern='delete_video'))  # New handler for delete video
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_name))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video_upload))
    application.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))
    application.add_handler(CallbackQueryHandler(show_commands, pattern='help'))  # Show commands handler
    application.add_handler(CallbackQueryHandler(remove_video, pattern='delete_.*'))  # New handler for removing video
    application.add_handler(CallbackQueryHandler(list_videos, pattern='list_videos'))
    application.add_handler(CallbackQueryHandler(send_video, pattern='^[a-fA-F0-9]{24}$'))  # Match video ID pattern

    application.run_polling()
    logger.info("Bot telah berjalan!")

if __name__ == '__main__':
    main()
