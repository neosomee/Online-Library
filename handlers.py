from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

router = Router()


class start(StatesGroup):
    name = State()
    age = State()
    number = State()



@router.message(F.text == 'Список книг')
async def nice(message: Message):
    await message.answer('Выберите автора',reply_markup=kb.spisok)


@router.callback_query(F.data == 'pushkin')
async def pushkin(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Вы выбрали категорию книг Пушкина')


@router.message(Command('start'))
async def register(message: Message, state: FSMContext):
    await message.answer('Добро пожаловать', reply_markup=kb.markup)
    await state.set_state(start.name)
    await message.answer('Введите ваше фамилию и имя')


@router.message(start.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(start.age)
    await message.answer('Введите ваш возраст')


@router.message(start.age)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(start.number)
    await message.answer('Введите ваш номер телефона',reply_markup=kb.get_number)


@router.message(start.number, F.contact)
async def register_number(message: Message, state:FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Ваше имя и фамилия: {data['name']}\nВаш возраст: {data['age']}\nНомер: {data['number']}')
    await state.clear