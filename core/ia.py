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
    Busca a transcrição de um vídeo do YouTube.

    IMPORTANTE:
    O agente deve enviar somente o ID do vídeo.

    Exemplo correto:
    21G-hvykfVo

    Exemplo errado:
    https://youtu.be/21G-hvykfVo
    """
    print(f"/n/n/noioioioi")
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
    model="kimi-k2.6:cloud",
    base_url=os.getenv("base_url"),
    temperature=0.7,
    client_kwargs={
        "headers": {"Authorization": f"Bearer {os.getenv('OLLAMA_KEY')}"}
    },
)

llm_com_ferramentas = llm.bind_tools(tools)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
Você é um assistente em português do Brasil.

Regras obrigatórias:

1. Nunca invente conteúdo.

2. Se o usuário enviar link do YouTube,
ou pedir resumo de vídeo,
você DEVE usar a ferramenta youtube.

3. Nunca responda apenas com o ID.

4. Sempre use a tool youtube para obter a transcrição.

5. A tool recebe somente o ID do vídeo.
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