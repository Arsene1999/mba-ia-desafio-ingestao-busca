import os, time
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres.vectorstores import PGVector
from langchain_core.prompts import PromptTemplate

load_dotenv()

embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

CONNECTION = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question):
  try:
    inicio = time.perf_counter()
    vector_store = PGVector(
        connection=CONNECTION,
        collection_name=COLLECTION_NAME,
        embeddings=embeddings,
    )
    
    docs = vector_store.similarity_search(question, k=10)
    
    contexto_formatado = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt_final = prompt.format(contexto=contexto_formatado, pergunta=question)
    
    print("\n--- RESPOSTA DA IA ---\n")
    resposta = llm.invoke(prompt_final)
    
    print(resposta.content )
    fim = time.perf_counter()
    print(f"Tempo de resposta: {fim - inicio:.2f} segundos\n")
    return True
  
  except Exception as e:
    print(f"Erro durante a busca: {e}")
    
    return False