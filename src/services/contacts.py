from datetime import date, timedelta
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import User
from src.repositories.contacts import ContactRepository
from src.schemas.contact import ContactCreate, ContactUpdate, ContactResponse


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def create_contact(self, contact: ContactCreate, user: User) -> ContactResponse:
        return await self.repository.create_contact(contact, user)

    async def get_contacts(
        self,
        limit: int = 10,
        offset: int = 0,
        user: User = None
    ) -> List[ContactResponse]:
        return await self.repository.get_contacts(limit, offset, user)

    async def get_contact(self, contact_id: int, user: User) -> Optional[ContactResponse]:
        return await self.repository.get_contact_by_id(contact_id, user)

    async def update_contact(
        self,
        contact_id: int,
        contact_update: ContactUpdate,
        user: User
    ) -> Optional[ContactResponse]:
        return await self.repository.update_contact(contact_id, contact_update, user)

    async def delete_contact(self, contact_id: int, user: User) -> Optional[ContactResponse]:
        return await self.repository.remove_contact(contact_id, user)

    async def get_upcoming_birthdays(self, user: User) -> List[ContactResponse]:
        """
        Отримання контактів з майбутніми днями народження
        """
        today = date.today()
        end_date = today + timedelta(days=7)
        return await self.repository.get_contacts_with_birthday_between(today, end_date, user)

    async def search_contacts(self, query: str, user: User) -> List[ContactResponse]:
        """
        Розширений пошук контактів з додатковою бізнес-логікою
        """
        contacts = await self.repository.search_contacts(query, user)
        # Тут можна додати додаткову логіку, наприклад:
        # - Сортування результатів за релевантністю
        # - Фільтрація результатів
        # - Обмеження кількості результатів
        return contacts

    async def get_birthday_contacts(self, days: int = 7) -> List[ContactResponse]:
        """
        Отримання контактів з днями народження на вказану кількість днів
        """
        today = date.today()
        end_date = today + timedelta(days=days)
        return await self.repository.get_contacts_with_birthday_between(today, end_date)
