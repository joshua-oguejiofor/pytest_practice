from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class TodoList(Base):
    __tablename__  = "todo_list"
    
    id: Mapped[int] = mapped_column(sa.Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    completed: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    
    
