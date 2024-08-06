from aiogram import Router, F, types
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMemberOwner, ChatMemberAdministrator

from bot.db.models.users import User
from bot.db.api import update_user


router = Router()


@router.message(F.chat.type.in_({"group", "supergroup"}), F.message_thread_id == 57)
async def antispam_handler(message: types.Message, user: User):

    user_permission = (await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).status
    if user_permission in [ChatMemberOwner, ChatMemberAdministrator, ChatMemberStatus.CREATOR]:
        return
    if user.count_posts == 2:
        await message.delete()
        await message.answer(
            text=f"@{message.from_user.username}, лимит постов превышен: <code>2</code>"
        )
        return

    if "@Mr_Perkins" not in message.text:

        await message.delete()
        await message.answer(
            text=f"@{message.from_user.username}, добавьте гаранта @Mr_Perkins в пост."
        )
        return

    new_count_posts = user.count_posts + 1
    await update_user(new_count_posts, message.from_user.id)
