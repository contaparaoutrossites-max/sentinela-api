import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from models import AnaliseResponse
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Carrega a chave do arquivo .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada no .env")

# Configura a IA
genai.configure(api_key=api_key)

async def analisar_ameaca_ia(texto: str) -> AnaliseResponse:
    print(f"--- INICIANDO ANÁLISE COM GEMINI 2.5 FLASH ---")
    
    # ATUALIZADO: Usando o modelo disponível na sua lista de 2026
    model = genai.GenerativeModel('models/gemini-2.5-flash')

    # Configuração de segurança (para permitir analisar ameaças sem bloquear)
    configuracao_seguranca = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
    
    prompt = f"""
    Você é um especialista em Cibersegurança (SOC). Analise o texto abaixo.
    
    TEXTO: "{texto}"
    
    Responda EXATAMENTE neste formato JSON:
    {{
        "nivel_risco": (inteiro de 0 a 100),
        "classificacao": (string: "Seguro", "Spam", "Phishing", "Malware"),
        "justificativa": (string: explicação técnica curta em pt-br),
        "entidades": (lista de strings extraídas do texto)
    }}
    """

    try:
        # Chamada assíncrona
        response = await model.generate_content_async(
            prompt, 
            generation_config={"response_mime_type": "application/json"},
            safety_settings=configuracao_seguranca
        )
        
        print("--- IA RESPONDEU ---")
        
        # Tratamento extra caso venha alguma sujeira no JSON
        texto_limpo = response.text.replace("```json", "").replace("```", "").strip()
        dados = json.loads(texto_limpo)
        
        return AnaliseResponse(**dados)

    except Exception as e:
        print(f"ERRO NO GEMINI: {e}")
        return AnaliseResponse(
            nivel_risco=0,
            classificacao="ERRO DE API",
            justificativa=f"Falha técnica: {str(e)}",
            entidades=[]
        )