from pydantic import BaseModel, Field

#o que o user envia para a API
class AnaliseRequest(BaseModel):
    texto: str = Field (..., min_length=10, description = "O texto suspeito (email, SMS, URL)")


#o que a API responde
class AnaliseResponse(BaseModel):
    nivel_risco: int #0 a 100
    classificacao: str # Seguro, Suspeito, Phishing
    justificativa: str
    entidades: list[str] = [] # Lista de nomes/locais encontrados