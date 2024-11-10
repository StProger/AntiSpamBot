from aiogram import Router, F, types, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMemberOwner, ChatMemberAdministrator, ChatPermissions
from aiogram.filters.command import Command
import asyncio

from datetime import datetime, timedelta

import pytz

from bot.db.models.users import User
from bot.db.api import (update_user,
                        delete_mes,
                        update_count_warnings,
                        update_last_message_id_work,
                        update_last_message_id_las_vegas, find_tg_id)
from bot.service.redis_serv.user import (set_message_id_work,
                                         get_message_id_work,
                                         set_message_id_las_vegas,
                                         get_message_id_las_vegas)


router = Router()


permissions_admins = [ChatMemberOwner, ChatMemberAdministrator, ChatMemberStatus.CREATOR,
                           ChatMemberStatus.ADMINISTRATOR]


# @router.message(Command("mes"), F.chat.type.in_({"group", "supergroup"}))
# async def mes(message: types.Message):
#
#     print(message.reply_to_message)


@router.message(Command("ban"), F.chat.type.in_({"group", "supergroup"}))
async def ban_member(message: types.Message, user: User, bot: Bot):

    user_permission = (await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).status
    print(f"Ban | Username: {message.from_user.username}, {user_permission}")
    if user_permission in permissions_admins or message.from_user.username == "GroupAnonymousBot":

        args = message.text.split()

        if len(args) > 2:
            reason = " ".join(args[2:])
        else:
            reason = None

        if message.reply_to_message:

            reply_message = message.reply_to_message

            user_reply_message = reply_message.from_user

            user_id = user_reply_message.id

            try:
                await bot.ban_chat_member(
                    chat_id=message.chat.id,
                    user_id=user_id
                )

                if reason:
                    text = (f"Пользователь ({user_id}) забанен.\n"
                            f"Причина: {reason}")
                else:
                    text = f"Пользователь ({user_id}) забанен."

                mes = await message.answer(text)
                asyncio.create_task(delete_mes(mes))
            except Exception as e:

                print(f"Не смог забанить. Ошибка {e}")

        else:

            if args[1].isdigit():

                user_id = int(args[1])

                try:
                    await bot.ban_chat_member(
                        chat_id=message.chat.id,
                        user_id=user_id
                    )

                    if reason:
                        text = (f"Пользователь ({user_id}) забанен.\n"
                                f"Причина: {reason}")
                    else:
                        text = f"Пользователь ({user_id}) забанен."

                    mes = await message.answer(text)
                    asyncio.create_task(delete_mes(mes))
                except Exception as e:

                    print(f"Не смог забанить. Ошибка {e}")
                await message.delete()
                return

            username_user = args[1]

            user_for_ban: User = await find_tg_id(username_user.replace("@", ""))

            try:
                await bot.ban_chat_member(
                    chat_id=message.chat.id,
                    user_id=user_for_ban.tg_id
                )

                if reason:
                    text = (f"🚫 Пользователь ({user_for_ban.tg_id}) забанен. 🚫\n"
                            f"Причина: {reason}")
                else:
                    text = f"🚫 Пользователь ({user_for_ban.tg_id}) забанен. 🚫"

                mes = await message.answer(text)
                asyncio.create_task(delete_mes(mes))
            except Exception as e:

                print(f"Не смог забанить. Ошибка {e}")

    await message.delete()


@router.message(Command("warn"), F.chat.type.in_({"group", "supergroup"}))
async def warn_user(message: types.Message, user: User, bot: Bot):
    print(message.from_user.username)
    print(message.from_user.id)
    user_permission = (await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).status
    print(user_permission)
    if user_permission in permissions_admins or message.from_user.username == "GroupAnonymousBot":
        print("Админ, делаю предупреждение")
        args = message.text.split()

        if len(args) > 2:
            reason = " ".join(args[2:])
        else:
            reason = None

        username = args[1].replace("@", "")

        if message.reply_to_message:
            print("Ответ на сообщение есть")
            try:
                reply_message = message.reply_to_message

                user_reply_message = reply_message.from_user

                user_id = user_reply_message.id

                user_to_warn = await find_tg_id(user_reply_message.username)

                if user_to_warn:

                    if user_to_warn.warning_count == 2:
                        try:
                            await bot.ban_chat_member(
                                chat_id=message.chat.id,
                                user_id=user_id
                            )
                            await message.delete()
                            return

                        except Exception as e:

                            print(f"Не смог забанить. Ошибка {e}")
                    await update_count_warnings(user_to_warn.tg_id, user_to_warn.warning_count + 1)

                    if reason:

                        text = (f"⚠️ @{username}, предупреждение. ⚠️\n"
                                f"Причина: {reason}")

                    else:

                        text = f"⚠️ @{username}, предупреждение. ⚠️"

                    await message.answer(
                        text=text
                    )
            except Exception as e:
                print(e)


        else:
            print("Нет ответа на сообщение")
            try:
                user_to_warn = await find_tg_id(username)

                if user_to_warn:

                    if user_to_warn.warning_count == 2:
                        try:
                            await bot.ban_chat_member(
                                chat_id=message.chat.id,
                                user_id=user_to_warn.tg_id
                            )
                            await message.delete()
                            return

                        except Exception as e:

                            print(f"Не смог забанить. Ошибка {e}")
                    await update_count_warnings(user_to_warn.tg_id, user_to_warn.warning_count + 1)

                    if reason:

                        text = (f"⚠️ @{username}, предупреждение. ⚠️\n"
                                f"Причина: {reason}")

                    else:

                        text = f"⚠️ @{username}, предупреждение. ⚠️"

                    await message.answer(
                        text=text
                    )
            except Exception as e:
                print(e)

        await message.delete()


@router.message(Command("mute"), F.chat.type.in_({"group", "supergroup"}))
async def mute_user(message: types.Message, user: User, bot: Bot):

    user_permission = (await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).status
    if user_permission in permissions_admins or message.from_user.username == "GroupAnonymousBot":

        args = message.text.split()

        if len(args) > 3:
            reason = " ".join(args[3:])
        else:
            reason = None

        username = args[1].replace("@", "")

        interval = int(args[2])

        if reason:
            text = (f"🔇 @{username} мут на {interval} часов. 🔇\n"
                    f"Причина: {reason}")
        else:

            text = f"🔇 @{username} мут на {interval} часов. 🔇"

        until_date = datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(hours=interval)

        if message.reply_to_message:

            reply_message = message.reply_to_message

            user_reply_message = reply_message.from_user

            user_id = user_reply_message.id

            try:
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=user_id,
                    permissions=ChatPermissions(),
                    until_date=until_date
                )

                await message.answer(
                    text=text
                )
            except Exception as e:
                print(e)

        else:

            user_to_mute = await find_tg_id(username)

            if user_to_mute:
                try:
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=user_to_mute.tg_id,
                        permissions=ChatPermissions(),
                        until_date=until_date
                    )

                    await message.answer(
                        text=text
                    )
                except Exception as e:
                    print(e)

        await message.delete()


@router.message(F.chat.type.in_({"group", "supergroup"}), F.message_thread_id.in_({None,}))
async def antispam_handler(message: types.Message, user: User, bot: Bot):

    user_permission = (await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).status
    if user_permission in permissions_admins or message.from_user.username == "GroupAnonymousBot":
        return
    print(f"Сообщение от бота: {message.from_user.is_bot}")
    if message.from_user.is_bot and message.from_user.username != "GroupAnonymousBot":
        await message.delete()
        await message.bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=message.from_user.id
        )
        return
    low_text = message.text.lower()
    if len(message.text) >= 100:

        if user.count_posts == 2:
            if user.warning_count == 2:
                try:
                    await bot.ban_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id
                    )
                    await message.delete()
                    return
                    # print("Забанил")
                    # await message.answer(f"Пользователь ({message.from_user.id}) забанен.")
                except Exception as e:

                    print(f"Не смог забанить. Ошибка {e}")

            # if user.last_message_id_work:
            #     try:
            #         await bot.delete_message(
            #             chat_id=message.chat.id,
            #             message_id=user.last_message_id_work
            #         )
            #     except:
            #         pass
            if (await get_message_id_work()):
                try:
                    await bot.delete_message(
                        chat_id=message.chat.id,
                        message_id=(await get_message_id_work())
                    )
                except:
                    pass
            await message.delete()
            mes = await message.answer(
                text=f"@{message.from_user.username} ({message.from_user.id}), лимит постов превышен: <code>2</code>"
            )
            await set_message_id_work(mes.message_id)
            await update_count_warnings(message.from_user.id, user.warning_count + 1)
            await update_last_message_id_work(message.from_user.id, mes.message_id)
            # asyncio.create_task(delete_mes(mes))
            return

        if "@Mr_Perkins" not in message.text:

            await message.delete()
            # if user.last_message_id_work:
            #     try:
            #         await bot.delete_message(
            #             chat_id=message.chat.id,
            #             message_id=user.last_message_id_work
            #         )
            #     except:
            #         pass
            if (await get_message_id_work()):
                try:
                    await bot.delete_message(
                        chat_id=message.chat.id,
                        message_id=(await get_message_id_work())
                    )
                except:
                    pass

            if user.warning_count == 2:
                try:
                    await bot.ban_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id
                    )
                    await message.delete()
                    return
                    # print("Забанил")
                    # await message.answer(f"Пользователь ({message.from_user.id}) забанен.")
                except Exception as e:

                    print(f"Не смог забанить. Ошибка {e}")
            mes = await message.answer(
                text=f"@{message.from_user.username} ({message.from_user.id}), не забывайте добавлять в пост гаранта @Mr_Perkins."
            )
            await update_count_warnings(message.from_user.id, user.warning_count + 1)
            await set_message_id_work(mes.message_id)
            await update_last_message_id_work(message.from_user.id, mes.message_id)
            # asyncio.create_task(delete_mes(mes))
            return
        new_count_posts = user.count_posts + 1
        await update_user(new_count_posts, message.from_user.id)
    elif (("куплю" in low_text) or ("продам" in low_text)
          or ("услуги" in low_text) or ("услуга" in low_text)
          or ("возьму" in low_text) or ("нужен" in low_text)
          or ("приму" in low_text) or ("нужны" in low_text)
          or ("подработка" in low_text) or ("работа" in low_text)
          or ("агенство" in low_text) or ("связь" in low_text)
          or ("подробнее" in low_text) or ("куплб" in low_text)
          or ("ищу" in low_text)):

        # if user.last_message_id_work:
        #     try:
        #         await bot.delete_message(
        #             chat_id=message.chat.id,
        #             message_id=user.last_message_id_work
        #         )
        #     except:
        #         pass
        if (await get_message_id_work()):
            try:
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=(await get_message_id_work())
                )
            except:
                pass

        if user.count_posts == 2:
            await message.delete()
            if user.warning_count == 2:
                try:
                    await bot.ban_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id
                    )
                    await message.delete()
                    return
                    # print("Забанил")
                    # await message.answer(f"Пользователь ({message.from_user.id}) забанен.")
                except Exception as e:

                    print(f"Не смог забанить. Ошибка {e}")
            mes = await message.answer(
                text=f"@{message.from_user.username} ({message.from_user.id}), лимит постов превышен: <code>2</code>"
            )
            await update_count_warnings(message.from_user.id, user.warning_count + 1)
            await set_message_id_work(mes.message_id)
            await update_last_message_id_work(message.from_user.id, mes.message_id)
            # asyncio.create_task(delete_mes(mes))
            return

        if "@Mr_Perkins" not in message.text:

            # if user.last_message_id_work:
            #     try:
            #         await bot.delete_message(
            #             chat_id=message.chat.id,
            #             message_id=user.last_message_id_work
            #         )
            #     except:
            #         pass
            if (await get_message_id_work()):
                try:
                    await bot.delete_message(
                        chat_id=message.chat.id,
                        message_id=(await get_message_id_work())
                    )
                except:
                    pass
            await message.delete()
            if user.warning_count == 2:
                try:
                    await bot.ban_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id
                    )
                    await message.delete()
                    return
                    # print("Забанил")
                    # await message.answer(f"Пользователь ({message.from_user.id}) забанен.")
                except Exception as e:

                    print(f"Не смог забанить. Ошибка {e}")
            mes = await message.answer(
                text=f"@{message.from_user.username} ({message.from_user.id}), не забывайте добавлять в пост гаранта @Mr_Perkins."
            )
            await update_count_warnings(message.from_user.id, user.warning_count + 1)
            await update_last_message_id_work(message.from_user.id, mes.message_id)
            await set_message_id_work(mes.message_id)
            # asyncio.create_task(delete_mes(mes))
            return
        new_count_posts = user.count_posts + 1
        await update_user(new_count_posts, message.from_user.id)


@router.message(F.chat.type.in_({"group", "supergroup"}), F.message_thread_id.in_({67}))
async def antispam_handler(message: types.Message, user: User, bot: Bot):

    user_permission = (await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).status
    print(f"Username: {message.from_user.username}, {user_permission}")
    if user_permission in [ChatMemberOwner, ChatMemberAdministrator, ChatMemberStatus.CREATOR,
                           ChatMemberStatus.ADMINISTRATOR] or message.from_user.username == "GroupAnonymousBot":
        return
    print(f"Сообщение от бота: {message.from_user.is_bot}")
    if message.from_user.is_bot and message.from_user.username != "GroupAnonymousBot":
        await message.delete()
        await message.bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=message.from_user.id
        )
        return
    low_text = message.text.lower()
    if len(message.text) > 100:

        await message.delete()
        if user.warning_count == 2:
            try:
                await bot.ban_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id
                )
                await message.delete()
                return
                # print("Забанил")
                # await message.answer(f"Пользователь ({message.from_user.id}) забанен.")
            except Exception as e:

                print(f"Не смог забанить. Ошибка {e}")
        # if user.last_message_id_las_vegas:
        #     try:
        #         await bot.delete_message(
        #             chat_id=message.chat.id,
        #             message_id=user.last_message_id_las_vegas
        #         )
        #     except Exception as e:
        #         pass
        last_message_id = await get_message_id_las_vegas()
        if last_message_id:
            try:
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=last_message_id
                )
            except:
                pass

        mes = await message.answer(
            text=f"@{message.from_user.username} ({message.from_user.id}), предлагайте услуги в ветке <b>WORK/УСЛУГИ</b>. И не забывайте писать гаранта @Mr_Perkins"
        )
        await update_count_warnings(message.from_user.id, user.warning_count + 1)
        await update_last_message_id_las_vegas(message.from_user.id, mes.message_id)
        await set_message_id_las_vegas(mes.message_id)
        # asyncio.create_task(delete_mes(mes))
        return

    elif (("куплю" in low_text) or ("продам" in low_text)
          or ("услуги" in low_text) or ("услуга" in low_text)
          or ("возьму" in low_text) or ("нужен" in low_text)
          or ("приму" in low_text) or ("нужны" in low_text)
          or ("подработка" in low_text) or ("работа" in low_text)
          or ("связь" in low_text) or ("агенство" in low_text)
          or ("подробнее" in low_text) or ("куплб" in low_text)
          or ("ищу" in low_text)):
        if user.warning_count == 2:
            try:
                await bot.ban_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id
                )
                await message.delete()
                return
                # print("Забанил")
                # await message.answer(f"Пользователь ({message.from_user.id}) забанен.")
            except Exception as e:

                print(f"Не смог забанить. Ошибка {e}")
        # if user.last_message_id_las_vegas:
        #     try:
        #         await bot.delete_message(
        #             chat_id=message.chat.id,
        #             message_id=user.last_message_id_las_vegas
        #         )
        #     except Exception as e:
        #         pass
        last_message_id = await get_message_id_las_vegas()
        if last_message_id:
            try:
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=last_message_id
                )
            except:
                pass
        await message.delete()
        mes = await message.answer(
            text=f"@{message.from_user.username} ({message.from_user.id}), предлагайте услуги в ветке <b>WORK/УСЛУГИ</b>. И не забывайте писать гаранта @Mr_Perkins"
        )
        await update_count_warnings(message.from_user.id, user.warning_count + 1)
        await update_last_message_id_las_vegas(message.from_user.id, mes.message_id)
        await set_message_id_las_vegas(mes.message_id)
        # asyncio.create_task(delete_mes(mes))
        return



