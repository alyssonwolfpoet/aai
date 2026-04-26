from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
import os
from langchain.agents import create_agent
from dotenv import load_dotenv
import json
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.tools import tool

load_dotenv()


@tool
def youtube(video_id: str) -> str:
    """
    Use esta ferramenta SOMENTE quando precisar buscar a transcrição
    de um vídeo do YouTube.

    IMPORTANTE:
    O agente deve enviar APENAS o ID do vídeo,
    e NÃO a URL completa.

    Exemplo correto:
    yinSh2daMMY

    Exemplo errado:
    https://www.youtube.com/watch?v=yinSh2daMMY

    Entrada esperada:
    - video_id (str): ID único do vídeo no YouTube

    Saída:
    - Texto completo da transcrição do vídeo
    """

    try:
        # Buscar transcrição do vídeo
        transcript = YouTubeTranscriptApi().fetch(
            video_id,
            languages=["pt", "en"]
        )

        # Juntar todo o texto da legenda
        texto = " ".join(
            [item.text for item in transcript]
        )

        if not texto.strip():
            return "Não foi encontrada transcrição para este vídeo."

        return f"Transcrição encontrada:\n\n{texto}"

    except Exception as e:
        return f"Erro ao buscar transcrição do vídeo: {str(e)}"

tools = [youtube]

llm = ChatOllama(
    model="gemma3:4b-cloud",
    base_url=os.getenv("base_url"),
    temperature=0.7,
    client_kwargs={
        "headers": {"Authorization": f"Bearer {os.getenv('OLLAMA_KEY')}"}
    },
)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
Você é um agente com acesso a ferramentas.

REGRA OBRIGATÓRIA:

Se o usuário enviar link de YouTube,
ou pedir resumo de vídeo,
ou pedir análise de vídeo,
você DEVE obrigatoriamente chamar a ferramenta youtube.

NUNCA responda apenas com o ID.

NUNCA responda com a URL.

Você deve usar a tool youtube passando somente o ID.

Exemplo:

Usuário:
Resuma esse vídeo:
https://youtu.be/21G-hvykfVo

Você deve fazer:

youtube("21G-hvykfVo")

e depois responder com base na transcrição retornada.

Essa regra é obrigatória.
"""
)

history = []

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente que responde em PT-BR de forma simples e direta. Use o histórico para contexto."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

promptAgent = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente que responde em PT-BR de forma simples e direta. Use o histórico para contexto."),
    MessagesPlaceholder(variable_name="history"),
])


chain = prompt | llm



def llmcall(user_input):
     result = chain.invoke({
        "input": user_input,
        "history": history
    })
     history.append(HumanMessage(content=user_input))
     history.append(AIMessage(content=result.content))
     
    
     return result.content,history

def agentCall(user_input):
    result = agent.invoke({"messages": [HumanMessage(user_input)]})

    return result