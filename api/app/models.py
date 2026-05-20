from sqlalchemy import Column, String, Integer, DateTime, func
from app.database import Base


class URL(Base):
    __tablename__ = "urls"

    short_code = Column(String(20), primary_key=True, index=True)
    original_url = Column(String(2048), nullable=False)
    click_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Why index=True on short_code?
# Every redirect query does WHERE short_code = ?
# Without an index that's a full table scan = slow at scale
