# © Silicon-Developer

import os
import asyncio
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def upload_image_requests(image_path):
    upload_url = "https://envs.sh"

    try:
        with open(image_path, 'rb') as file:
            files = {'file': file} 
            response = requests.post(upload_url, files=files)

            if response.status_code == 200:
                return response.text.strip() 
            else:
                raise Exception(f"Upload failed with status code {response.status_code}")

    except Exception as e:
        print(f"Error during upload: {e}")
        return None
@Client.on_message(filters.command("upload") & filters.private)
async def upload_command(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("⚠️ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇᴅɪᴀ ᴜɴᴅᴇʀ 𝟻 ᴍʙ") 
        return

    if replied.media and hasattr(replied, 'file_size'):
        if replied.file_size > 5242880:
            await message.reply_text("⚠️ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇᴅɪᴀ ᴜɴᴅᴇʀ 𝟻 ᴍʙ")
            return

    rahul = await replied.download()

    uploading_message = await message.reply_text("<code>ᴜᴘʟᴏᴀᴅɪɴɢ...</code>")

    try:
        url = upload_image_requests(rahul)
        if not url:
            raise Exception("Failed to upload file.")
    except Exception as error:
        await uploading_message.edit_text(f"Upload failed: {error}")
        return

    try:
        os.remove(rahul)
    except Exception as error:
        print(f"Error removing file: {error}")

    await uploading_message.delete()
    techifybots=await message.reply_photo(
        photo=f'{url}',
        caption=f"<b>ʏᴏᴜʀ ᴄʟᴏᴜᴅ ʟɪɴᴋ ᴄᴏᴍᴘʟᴇᴛᴇᴅ 👇</b>\n\n𝑳𝒊𝒏𝒌 :-\n\n<code>{url}</code>\n\n<b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ - @AKMOVIEBOTZ</b>",
        #disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(text="• ᴏᴘᴇɴ ʟɪɴᴋ •", url=url),
            InlineKeyboardButton(text="• sʜᴀʀᴇ ʟɪɴᴋ •", url=f"https://telegram.me/share/url?url={url}")
        ], [
            InlineKeyboardButton(text="❌   ᴄʟᴏsᴇ   ❌", callback_data="close_data")
        ]])
   )
    await asyncio.sleep(120)
    await techifybots.delete()
