import aiosqlite
import asyncio
import string

from dataclasses import dataclass
from typing import Optional

from rubpy.bot import BotClient, filters
from rubpy.bot.models import Update

from collections import OrderedDict



@dataclass
class GroupData:
    chat_id: int
    owner_guid: str
    start_time: float = 0.0
    is_vip: bool = False

@dataclass
class GroupPermissions:
    chat_id: int
    change_info: bool = True
    pin_message: bool = True
    delete_message: bool = True
    delete_member: bool = True
    add_admin: bool = True
    change_acc: bool = True

@dataclass
class filterGroup:
    chat_id: int
    filters: str = ''

@dataclass
class blockedConGroup:
    chat_id: int
    blocked_contract: str = ''

@dataclass
class adminGroup:
    chat_id: int
    user_guid: str = ''

class ErrorHandler:
    @staticmethod
    def handle_db_error(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)

            except Exception as e:
                print('Erorr in db database: ', e)
                return False
        
        return wrapper
    

class GlobalClass:
    ADMINS = []
    def __init__(self, bot:BotClient = None, message:Update = None):
        self.bot = bot
        self.message = message

    @property
    def text(self) -> str:
        return self.message.new_message.text
        
    @property
    def is_link(self) -> bool:
        link_indicators = {'http://', 'https://', 'rubika.ir', '@', 'www.'}
        return any(indicator in self.text.lower() for indicator in link_indicators)
    
    @property
    def is_code(self):
        return True if len(self.text) > 500 else False

    @property
    def is_badword(self) -> bool:
        punctuations = string.punctuation + '؟،«»؛…–—'
        translator = str.maketrans('', '', punctuations)
        text = self.text.translate(translator)
        link_indicators = {'بیو', 'چک', 'پی', 'کیر', 'کص', 'کس', 'جنده', 'مادر خراب', 'کون'}
        return any(indicator in text for indicator in link_indicators)

class CachedDatabase:
    async def is_installed(self, chat_id):
        pass


class Database:
    def __init__(self, name: str = 'database.db'):
        self.name = name
        self.lock = asyncio.Lock()
    
    async def _ensure_connection(self):
        conn = await aiosqlite.connect(self.name, timeout=30)
        await conn.execute("PRAGMA foreign_keys = ON;")
        await conn.execute("PRAGMA journal_mode = WAL;")
        return conn
    
    @ErrorHandler.handle_db_error
    async def Insert_data(self, data: tuple, table_name: str = 'group_data') -> bool:
        """
        tables : group_data , group_permissions, group_admins, group_filters, group_blocked_contracts
        """

        async with self.lock:
            db = await self._ensure_connection()
            await db.execute(f"INSERT OR IGNORE INTO {table_name} VALUES({','.join(['?']*len(data))})",data)
            await db.commit()
            await db.close()
            return True

    
    @ErrorHandler.handle_db_error
    async def select_data(self, chat_id: str, table_name: str = 'group_data', data_type:str = 'chat_id') -> Optional[tuple]:
        """
        tables : group_data , group_permissions, group_admins, group_filters, group_blocked_contracts
        """
        async with self.lock:
            db = await self._ensure_connection()
            async with db.execute(f"SELECT * FROM {table_name} WHERE {data_type}=?", (chat_id,)) as cursor:
                result = await cursor.fetchone()

            await db.close()
            return result if result else False
    
    @ErrorHandler.handle_db_error
    async def update_data(self, chat_id: str, column: str, value: str, table_name: str = 'group_data') -> bool:
        async with self.lock:
            db = await self._ensure_connection()
            await db.execute(f"UPDATE {table_name} SET {column}=? WHERE chat_id=?", (value, chat_id))
            await db.commit()
            await db.close()
            return True