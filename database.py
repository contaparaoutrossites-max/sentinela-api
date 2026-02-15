from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Cria o arquivo do banco localmente (igual ao .mdf do SQL Server LocalDB)
DATABASE_URL = "sqlite+aiosqlite:///./sentinela.db"

# O Engine é quem gerencia as conexões
engine = create_async_engine(DATABASE_URL, echo=True)

# A Session é quem executa as queries (igual ao DbContext do C#)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base para criar as tabelas (Models herdam disso)
Base = declarative_base()

# Dependência para injetar o banco nas rotas (Dependency Injection)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session