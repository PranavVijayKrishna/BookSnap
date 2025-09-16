from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models
import json

# Create
async def create_book_record(db: AsyncSession, filename: str, extracted_text: str, cleaned_text: str, book_info: dict):
    
    db_record = models.BookRecord(
        filename = filename, 
        extracted_text = extracted_text, 
        cleaned_text = cleaned_text, 
        book_info = json.dumps(book_info)
    )

    db.add(db_record)
    await db.commit()
    await db.refresh(db_record)

    return db_record


# Read
async def read_book_by_cleaned_text(db: AsyncSession, cleaned_text: str):

    result = await db.execute(select(models.BookRecord).where(models.BookRecord.cleaned_text == cleaned_text))
    book_record = result.scalars().first()

    if book_record:
        book_record.book_info = json.loads(book_record.book_info)

    return book_record


# Read all
async def read_all_books(db: AsyncSession):

    result = await db.execute(select(models.BookRecord))
    records = result.scalars().all()

    for record in records:
        record.book_info = json.loads(record.book_info)

    return records