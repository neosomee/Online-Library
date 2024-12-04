import aiosqlite
from app.classes import User, Book, Order
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Database:
    def __init__(self, path):
        self.path = path


# create tables
    async def create_users_table(self):
        async with aiosqlite.connect(self.path) as db:
            await db.execute('''
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER PRIMARY KEY NOT NULL,
	"fullname"	TEXT,
	"age"	INTEGER,
    "number"	TEXT,
    "book_id"   INTEGER
);
''')
            await db.commit()


    async def create_books_table(self):
        async with aiosqlite.connect(self.path) as db:
            await db.execute('''
CREATE TABLE IF NOT EXISTS "books" (
	"id"	INTEGER PRIMARY KEY NOT NULL,
	"title"	TEXT,
	"author"	TEXT,
    "category"	TEXT
);
''')
            await db.commit()
    

    async def create_order_table(self):
        async with aiosqlite.connect(self.path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    order_info TEXT
                );
            ''')
            await db.commit()
#


# user funcs
    async def get_user(self, user_id):
        async with aiosqlite.connect(self.path) as db:
            async with db.execute(f"SELECT * FROM users WHERE id = {user_id}") as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return
                user = User()
                user.id = int(row[0])
                user.fullname = row[1]
                user.age = int(row[2])
                user.number = row[3]
                user.book_id = int(row[4])
                return user


    async def del_user(self, user_id):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(f"DELETE FROM users WHERE id = {user_id}")
            await db.commit()


    async def save_user(self, user: User):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT INTO users (id, fullname, age, number, book_id) VALUES (?, ?, ?, ?, -1)",
                (user.id, user.fullname, user.age, user.number)
            )
            await db.commit()


    async def edit_user(self, user: User):
        async with aiosqlite.connect(self.path) as db:
            prev = await self.get_user(user.id)
            
            if user.fullname is None:
                user.fullname = prev.fullname
            if user.age is None:
                user.age = prev.age
            if user.number is None:
                user.number = prev.number
            if user.book_id is None:
                user.book_id = prev.book_id
            
            await db.execute(
                "UPDATE users SET fullname = ?, age = ?, number = ?, book_id = ? WHERE id = ?",
                (user.fullname, user.age, user.number, user.book_id, user.id)
            )
            await db.commit()
#


# book funcs
    async def add_book(self, book: Book):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT INTO books (id, title, author, category) VALUES (?, ?, ?, ?)",
                (book.id, book.title, book.author, book.category)
            )
            await db.commit()


    async def del_book(self, book_id):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(f"DELETE FROM books WHERE id = {book_id}")
            await db.commit()


    async def get_book(self, book_id):
        async with aiosqlite.connect(self.path) as db:
            async with db.execute(f"SELECT * FROM books WHERE id = {book_id}") as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return
                book = Book()
                book.id = int(row[0])
                book.title = row[1]
                book.author = row[2]
                book.category = row[3]
                return book


    async def get_books(self):
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT * FROM books") as cursor:
                rows = await cursor.fetchall()
                books = []
                for row in rows:
                    book = Book()
                    book.id = int(row[0])
                    book.title = row[1]
                    book.author = row[2]
                    book.category = row[3]
                    books.append(book)
                return books


    async def get_books_kb(self):
        books = await self.get_books()
        builder = InlineKeyboardBuilder()
        for i in books:
            builder.button(text=f"{i.title} - {i.author}", callback_data=f"book_{i.id}")
        builder.adjust(1)
        return builder.as_markup(resize_keyboard=True)


# order books 
    
    async def insert_order(self, order: Order):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                '''
                INSERT INTO orders (user_id, order_info)
                VALUES (:user_id, :order_info);
                ''',
                {'user_id': order.user_id, 'order_info': order.order}
            )
            await db.commit()