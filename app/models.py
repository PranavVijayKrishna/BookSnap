from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class BookRecord(Base):
    __tablename__ = "book_records"

    id = Column(Integer, primary_key = True, index = True)
    filename = Column(String, nullable = True)
    extracted_text = Column(Text, nullable = True)
    cleaned_text = Column(Text, unique = True, index = True)
    book_info = Column(Text, nullable = True)
    created_at = Column(DateTime(timezone = True), server_default = func.now())


