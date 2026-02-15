from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime

class AnaliseLog(Base):
    __tablename__="analises" #nome da tabela

    id = Column(Integer, primary_key=True, index=True)
    data_analise = Column(DateTime, default=datetime.utcnow)

    #entrada
    texto_original = Column(Text)

    #saida ia
    nivel_risco = Column(Integer)
    classificacao = Column(String)
    justificativa = Column(Text)
    entidades_encontradas = Column(Text, nullable=True)
