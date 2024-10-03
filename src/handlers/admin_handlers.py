import logging
import sqlite3 as sq
from src.database import database

from src.keyboards import admin_keyboards
from src import req, config, banwords

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ChatPermissions
from aiogram.fsm.context import FSMContext

rt = Router()
bot = Bot(token=config.BOT_TOKEN)
db = sq.connect(config.database_path)
cur = db.cursor()

admin = database.get_admin()


@rt.message(Command("start"))
async def admin_panel(message: Message, state: FSMContext):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        if str(user_id) in str(admin):
            await message.answer("✅ | Вы вошли в админ панель", reply_markup=await admin_keyboards.admin_keyboard())
            await state.set_state(state=None)
        else:
            await message.answer('Нет прав ❌')
    else:
        pass


@rt.callback_query(F.data == 'back')
async def admin_panel(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await call.message.edit_text("✅ | Вы вошли в админ панель", reply_markup=await admin_keyboards.admin_keyboard())
        await state.set_state(state=None)


@rt.callback_query(F.data == 'admins')
async def admin_panel(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await call.message.edit_text("✅ | Вы вошли в админ панель", reply_markup=await admin_keyboards.admins())
        await state.set_state(state=None)


@rt.callback_query(F.data == 'headman')
async def admin_panel(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await call.message.edit_text("✅ | Вы вошли в админ панель", reply_markup=await admin_keyboards.headman())
        await state.set_state(state=None)


@rt.callback_query(F.data == 'add_admin')
async def admin_pass(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await state.set_state(req.admin_add.password)
        await call.message.edit_text("🚧 | Чтобы добавить администратора, введите пароль", reply_markup=await admin_keyboards.back())


@rt.message(req.admin_add.password)
async def admin_id(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(req.admin_add.us)
    await message.delete()
    await message.answer("🚧 | Введите id администратора", reply_markup=await admin_keyboards.back())


@rt.message(req.admin_add.us)
async def admin_addd(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(us=message.text)
    p = await state.get_data()
    if p['password'] == config.password:
        with sq.connect(config.database_path):
            cur.execute("INSERT INTO admin (tg) VALUES (?)", (p['us'],))
            db.commit()
        await message.answer("✅ | Администратор добавлен", reply_markup=await admin_keyboards.admin_keyboard())
        await bot.promote_chat_member(chat_id=config.chat, user_id=p['us'], can_delete_messages=True)
        await bot.set_chat_administrator_custom_title(chat_id=config.chat, user_id=p['us'], custom_title='Администратор')
        await bot.send_message(p['us'], '😎 | Доступны команды администратора')
        await state.set_state(state=None)
    else:
        await message.answer("❌ | Неверный пароль", reply_markup=await admin_keyboards.admin_keyboard())
        await state.set_state(state=None)


@rt.callback_query(F.data == 'del_admin')
async def admin_pass(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await state.set_state(req.admin_del.password)
        await call.message.edit_text("🚧 | Чтобы удалить администратора, введите пароль", reply_markup=await admin_keyboards.back())


@rt.message(req.admin_del.password)
async def admin_id(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(req.admin_del.us)
    await message.delete()
    await message.answer("🚧 | Введите id администратора", reply_markup=await admin_keyboards.back())


@rt.message(req.admin_del.us)
async def admin_dell(message: Message, state: FSMContext):
    await state.update_data(us=message.text)
    p = await state.get_data()
    if p['password'] == config.password:
        with sq.connect(config.database_path):
            cur.execute("DELETE FROM admin WHERE tg = ?", (p['us'],))
            db.commit()
        await message.answer("✅ | Администратор удален", reply_markup=await admin_keyboards.admin_keyboard())
        await bot.send_message(p['us'], '❌ | Вам больше не доступны команды администратора')
        await bot.set_chat_administrator_custom_title(chat_id=config.chat, user_id=p['us'], custom_title='')
        await bot.promote_chat_member(chat_id=config.chat, user_id=p['us'], can_delete_messages=False)
    else:
        await message.answer("❌ | Неверный пароль", reply_markup=await admin_keyboards.admin_keyboard())
    await state.set_state(state=None)


@rt.callback_query(F.data == 'add_headman')
async def support_id(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await state.set_state(req.headman_add.us)
        await call.message.edit_text("🚧 | Введите id старосты", reply_markup=await admin_keyboards.back())


@rt.message(req.headman_add.us)
async def support_addd(message: Message, state: FSMContext):
    await state.update_data(us=message.text)
    p = await state.get_data()
    await message.answer("✅ | Староста добавлена", reply_markup=await admin_keyboards.admin_keyboard())
    await bot.promote_chat_member(chat_id=config.chat, user_id=p['us'], can_delete_messages=True)
    await bot.set_chat_administrator_custom_title(chat_id=config.chat, user_id=p['us'], custom_title='Староста')
    await state.set_state(state=None)


@rt.callback_query(F.data == 'del_headman')
async def support_id(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await state.set_state(req.headman_del.us)
        await call.message.edit_text("🚧 | Введите id старосты", reply_markup=await admin_keyboards.back())


@rt.message(req.headman_del.us)
async def support_dell(message: Message, state: FSMContext):
    await state.update_data(us=message.text)
    p = await state.get_data()
    await message.answer("✅ | Староста удалена", reply_markup=await admin_keyboards.admin_keyboard())
    await bot.set_chat_administrator_custom_title(chat_id=config.chat, user_id=p['us'], custom_title='')
    await bot.promote_chat_member(chat_id=config.chat, user_id=p['us'], can_delete_messages=False)
    await state.set_state(state=None)


@rt.callback_query(F.data == 'chat')
async def admin_panel(call: CallbackQuery):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await call.message.edit_text("✅ | Вы вошли в админ панель", reply_markup=await admin_keyboards.chat_settings())


@rt.callback_query(F.data == 'chat_on')
async def admin_panel(call: CallbackQuery):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        permissions = {
            'can_send_messages': True,
            'can_send_media_messages': True,
            'can_send_polls': True,
            'can_send_other_messages': True
        }
        new_permissions = ChatPermissions(**permissions)
        await bot.set_chat_permissions(chat_id=config.chat, permissions=new_permissions)
        await call.message.edit_text("✅ | Чат включен", reply_markup=await admin_keyboards.chat_off())


@rt.callback_query(F.data == 'chat_off')
async def admin_panel(call: CallbackQuery):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        permissions = {
            'can_send_messages': False,
            'can_send_media_messages': False,
            'can_send_polls': False,
            'can_send_other_messages': False
        }
        new_permissions = ChatPermissions(**permissions)
        await bot.set_chat_permissions(chat_id=config.chat, permissions=new_permissions)
        await call.message.edit_text("✅ | Чат отключен", reply_markup=await admin_keyboards.chat_on())


@rt.callback_query(F.data == 'info')
async def admin_panel(call: CallbackQuery):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        await call.message.edit_text("", reply_markup=await admin_keyboards.back())


@rt.message()
async def banword_filter(message: Message):
    if message.chat.type == 'private':
        return

    if not message.text:
        return

    message_text = message.text.lower()
    is_banword = any(banword in message_text for banword in banwords.ban_list)

    username = message.from_user.username or message.from_user.full_name

    if is_banword:
        try:
            await message.delete()
            logging.info(f"Удалено сообщение от пользователя {message.from_user.id} | {username}")
        except Exception as e:
            logging.error(f"Не удалось удалить сообщение: {e}")

        ban_count = await database.add_or_update_user(message.from_user.id, username)
        logging.info(f"Пользователь {username} ({message.from_user.id}) употребил мат {ban_count} раз")


@rt.callback_query(F.data == 'banwords')
async def show_banwords(call: CallbackQuery):
    user_id = call.message.chat.id
    if str(user_id) not in str(admin):
        await call.message.answer('Нет прав ❌')
    else:
        banned_users = await database.get_all_banned_users()

        if not banned_users:
            await call.message.edit_text("На данный момент нет пользователей, использовавших запрещённые слова. 😥", reply_markup=await admin_keyboards.back())
            return

        response = "📋 Список пользователей, использовавших запрещённые слова:\n\n"
        for user in banned_users:
            user_id, username, ban_count = user
            response += f"👤 <a href='tg://user?id={user_id}'>{username}</a> — {ban_count}\n"

        await call.message.reply(response, parse_mode="HTML", reply_markup=await admin_keyboards.back())


# @rt.callback_query(F.data == 'msg_from_bot')
# async def message_from_bot(call: CallbackQuery, state: FSMContext):
#     user_id = call.message.chat.id
#     if str(user_id) not in str(admin):
#         await call.message.answer('Нет прав ❌')
#     else:
#         await state.set_state(req.message123.zv)
#         await call.message.edit_text("Напишите сообщение, которое хотите отправить от лица бота (без картинок🥺)", reply_markup=await admin_keyboards.back())
#
#
# @rt.message(req.message123.zv)
# async def message_from_bot_send(message: Message, state: FSMContext):
#     await state.update_data(zv=message.text)
#     p = await state.get_data()
#     text = p['zv']
#     await bot.send_message(chat_id=config.chat, text=text)
#     await message.answer('Сообщение отправлено ✅', reply_markup=await admin_keyboards.back())
#     await state.set_state(state=None)
