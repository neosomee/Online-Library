from app.db import Database
from app.classes import Book, User, Order
import app.keyboards as kb
import app.states as states

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


db = Database(path="bot.db")
router = Router()
books = []


# Ordering book

@router.message(F.text == 'Заказать книгу')
async def order_book(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if not user:
        return
    await state.set_state(states.order_book.name)
    await message.answer("Напишите название книги")


# Обработчик состояния order_book.name
@router.message(states.order_book.name)
async def order_book_name(message: Message, state: FSMContext):
    book_name = message.text
    user_id = message.from_user.id

    # Сохраняем данные в базу данных
    order = Order(user_id=user_id, order=book_name)
    await db.insert_order(order)

    await state.clear()
    await message.answer(f'Ваш заказ на книгу "{book_name}" был успешно оформлен!')

# Main
@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if user:
        return await message.answer(f'Привет, {user.fullname}', reply_markup=kb.markup)
    await state.set_state(states.start.name)
    await message.answer('Введите ваше фамилию и имя')


@router.message(F.text == 'Личный кабинет')
async def profile(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if not user:
        return

    book = Book(title="Книга не найдена")

    if user.book_id and user.book_id != -1:
        book = await db.get_book(user.book_id)
        if book is None:
            book = Book(title="Книга не найдена")

    await message.answer(
        f"""
Вас зовут {user.fullname}
Ваш возраст: {user.age}
Ваш номер: {user.number}
{"Вы не брали ни одной книги" if user.book_id == -1 else f"Ваша последняя книга: {book.title}"}
""",
        reply_markup=kb.profile
    )


@router.message(F.text == 'Список книг')
async def nice(message: Message):
    global books
    user = await db.get_user(message.from_user.id)
    if not user:
        return
    books = await db.get_books()
    keyboard = await db.get_books_kb()
    if len(books) == 0:
        return await message.answer("Список книг пуст")
    await message.answer('Выберите книгу', reply_markup=keyboard)


@router.callback_query(F.data.startswith("book_"))
async def choose_book(message: Message, state: FSMContext):
    book = await db.get_book(int(message.data.split("_")[1]))
    user = await db.get_user(message.from_user.id)
    user.book_id = book.id
    await db.edit_user(user)
    await message.answer(f"Вы выбрали книгу '{book.title}'")


@router.message(F.text == 'Заказать книгу')
async def order_book(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if not user:
        return
    await state.set_state(states.order_book.name)
    await message.answer("Напишите название книги")


# Starting
@router.callback_query(F.data == 'reregister')
async def reregister(call: CallbackQuery,  state: FSMContext):
    await state.set_state(states.start.name)
    await call.message.answer('Введите ваше фамилию и имя')


@router.message(states.start.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(states.start.age)
    await message.answer('Введите ваш возраст')
    


@router.message(states.start.age)
async def register_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Введите корректный возраст")
    age = int(message.text)
    if age < 10 or age > 100:
        return await message.answer("Введите корректный возраст")
    await state.update_data(age=message.text)
    await state.set_state(states.start.number)
    await message.answer('Введите ваш номер телефона',reply_markup=kb.get_number)


@router.message(states.start.number, F.contact)
async def register_number(message: Message, state:FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    
    user = User(
        id=message.from_user.id,
        fullname=data["name"],
        age=data["age"],
        number=data["number"]
    )
    
    if await db.get_user(message.from_user.id):
        await db.edit_user(user)
    else:
        await db.save_user(user)
    
    await message.answer(f"""Информация успешно сохранена!
Ваше имя и фамилия: {data['name']}
Ваш возраст: {data['age']}
Номер: {data['number']}""", reply_markup=kb.markup)
    await state.clear()