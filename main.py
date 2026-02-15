from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 

# Importações dos seus outros arquivos
from database import engine, Base, get_db
from models import AnaliseRequest, AnaliseResponse
from models_db import AnaliseLog
from services import analisar_ameaca_ia

# Inicializa o App
app = FastAPI(
    title="Sentinela AI",
    description="API de detecção de Phishing e Ameaças",
    version="1.0.0"
)

# Cria as tabelas do banco ao iniciar
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def home():
    return {"status": "online", "message": "Sentinela AI operante"}

# --- ROTA DE ANÁLISE (QUE SALVA NO BANCO) ---
@app.post("/analisar", response_model=AnaliseResponse)
async def analisar_texto(request: AnaliseRequest, db: AsyncSession = Depends(get_db)):
    """
    1. Recebe texto
    2. Envia para IA
    3. Salva no Banco
    4. Retorna resultado
    """
    # 1. Chama a IA
    resultado = await analisar_ameaca_ia(request.texto)
    
    # 2. Cria o objeto do Banco (Mapeando o resultado da IA para a Tabela)
    # Truque: Se 'entidades' vier vazio, salvamos string vazia para não dar erro
    entidades_str = ",".join(resultado.entidades) if resultado.entidades else ""
    
    novo_log = AnaliseLog(
        texto_original=request.texto,
        nivel_risco=resultado.nivel_risco,
        classificacao=resultado.classificacao,
        justificativa=resultado.justificativa,
        entidades_encontradas=entidades_str
    )
    
    # 3. Salva efetivamente
    db.add(novo_log)
    await db.commit()
    await db.refresh(novo_log) # Atualiza para pegar o ID gerado
    
    print(f"--- SUCESSO! LOG SALVO NO BANCO COM ID: {novo_log.id} ---")

    return resultado

# --- ROTA DE HISTÓRICO ---
@app.get("/historico")
async def listar_historico(db: AsyncSession = Depends(get_db)):
    # Busca tudo no banco ordenado pelo mais recente
    query = select(AnaliseLog).order_by(AnaliseLog.id.desc())
    resultado = await db.execute(query)
    return resultado.scalars().all()
