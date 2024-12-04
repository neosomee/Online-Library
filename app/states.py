from aiogram.fsm.state import State, StatesGroup

class start(StatesGroup):
    name = State()
    age = State()
    number = State()


class order_book(StatesGroup):
    name = State()