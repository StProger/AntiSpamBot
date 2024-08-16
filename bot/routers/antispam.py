from aiogram import Router, F, types
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMemberOwner, ChatMemberAdministrator
import asyncio

from bot.db.models.users import User
from bot.db.api import update_user, delete_mes

router = Router()

@router.message(F.chat.type.in_({"group", "supergroup"}), F.message_thread_id.in_({None,}))
async def antispam_handler(message: types.Message, user: User):

    user_permission = (await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).status
    if user_permission in [ChatMemberOwner, ChatMemberAdministrator, ChatMemberStatus.CREATOR]:
        return
    low_text = message.text.lower()
    if len(message.text) > 100:

        if user.count_posts == 2:
            await message.delete()
            mes = await message.answer(
                text=f"@{message.from_user.username}, лимит постов превышен: <code>2</code>"
            )
            asyncio.create_task(delete_mes(mes))
            return

        if "@Mr_Perkins" not in message.text:

            await message.delete()
            mes = await message.answer(
                text=f"@{message.from_user.username}, не забывайте добавлять в пост гаранта @Mr_Perkins."
            )
            asyncio.create_task(delete_mes(mes))
            return
        new_count_posts = user.count_posts + 1
        await update_user(new_count_posts, message.from_user.id)
    elif (("куплю" in low_text) or ("продам" in low_text)
          or ("услуги" in low_text) or ("услуга" in low_text)
          or ("возьму" in low_text) or ("нужен" in low_text)
          or ("приму" in low_text) or ("нужны" in low_text)
          or ("подработка" in low_text) or ("работа" in low_text)):

        if user.count_posts == 2:
            await message.delete()
            mes = await message.answer(
                text=f"@{message.from_user.username}, лимит постов превышен: <code>2</code>"
            )
            asyncio.create_task(delete_mes(mes))
            return

        if "@Mr_Perkins" not in message.text:

            await message.delete()
            mes = await message.answer(
                text=f"@{message.from_user.username}, не забывайте добавлять в пост гаранта @Mr_Perkins."
            )
            asyncio.create_task(delete_mes(mes))
            return
        new_count_posts = user.count_posts + 1
        await update_user(new_count_posts, message.from_user.id)


@router.message(F.chat.type.in_({"group", "supergroup"}), F.message_thread_id.in_({47,}))
async def antispam_handler(message: types.Message, user: User):

    user_permission = (await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).status
    if user_permission in [ChatMemberOwner, ChatMemberAdministrator, ChatMemberStatus.CREATOR]:
        return
    low_text = message.text.lower()
    if len(message.text) > 100:

        await message.delete()
        mes = await message.answer(
            text=f"@{message.from_user.username}, предлагайте услуги в ветке <b>WORK/УСЛУГИ</b>. И не забывайте писать гаранта @Mr_Perkins"
        )
        asyncio.create_task(delete_mes(mes))
        return

    elif (("куплю" in low_text) or ("продам" in low_text)
          or ("услуги" in low_text) or ("услуга" in low_text)
          or ("возьму" in low_text) or ("нужен" in low_text)
          or ("приму" in low_text) or ("нужны" in low_text)
          or ("подработка" in low_text) or ("работа" in low_text)):

        await message.delete()
        mes = await message.answer(
            text=f"@{message.from_user.username}, предлагайте услуги в ветке <b>WORK/УСЛУГИ</b>. И не забывайте писать гаранта @Mr_Perkins"
        )
        asyncio.create_task(delete_mes(mes))
        return
