from fastapi import FastAPI, Response, status
from pydantic import BaseModel                      # base para criar a classe, mandar informação direto
from datetime import datetime
from operator import attrgetter

app = FastAPI()

lista = []

# Classe com herança, para usar na API
class Atendimento(BaseModel):                       
    posicao: int | None = None                      #informações não obrigatórias 
    nome: str                                       #campo obrigatório.
    prioridade: str                                 #campo obrigatório.
    chegada: datetime | None = datetime.today()     # se não passar a data, assume a data atual.
    atendido: bool | None = False                   # setar o atendimento com falso, caso não passe.
    
# raiz do projeto API / #async - método assincrono.
@app.get("/")                                       
async def root():                                   
    return {"api funcionando..."}

# Mostrar a fila de atendimento.
@app.get("/fila")
async def getFila():
    return {"fila": lista}

# Mostrar a fila de atendimento passando um ID / Apresentando erro 404 quando não tiver ninguém na fila
@app.get("/fila/{id}")
async def getFilaById(id : int,response: Response):
    if len(lista) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Erro": "fila vazia"}

    atendimento = None
    
    for x in lista:
        if x.posicao == id:
            atendimento = x

    if atendimento == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Erro": "Cliente não encontrado neste posição da fila"}
    
    return {"atendimento": atendimento}

# Atribui atendimento ao primeiro da fila, alterando o status para TRUE.
@app.put("/fila")
async def put():
    for x in lista:
        if x.posicao != 0 :
            x.posicao = x.posicao -1
        if x.posicao == 0:
            x.atendido = True
    return {"fila": lista}
        
# Adiciona uma nova pessoa na fila.
@app.post("/fila")
async def getFilaById(atendimento: Atendimento, response: Response):
    
    if len(atendimento.nome) == 0:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"Erro": "Nome é obrigatório"}
    if len(atendimento.nome) > 20:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"Erro": "Nome deve possuir no máximo 20 caracteres"}
    
    if atendimento.prioridade != 'P' and atendimento.prioridade != 'N':
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"Erro": "tipo de atendimento deve ser caracter unico N (Normal) ou P (Prioritário)"}
    
    if len(lista) == 0:
        atendimento.posicao = 1
    else:
        temp =  max(lista, key=attrgetter('posicao')) #Isso vai procurar e retornar na lista o maior valor do atributo 'posicao'
        atendimento.posicao = temp.posicao + 1

    lista.append(atendimento)
    
    return {"atendimento": atendimento}

# Deleta uma pessoa da fila com tratamento de ID inixistente.
@app.delete("/fila/{id}")
async def delete(id: int,response: Response):
    if len(lista) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Erro": "fila vazia"}
    
    atendimento = None
    
    for x in lista:
        if atendimento != None:
            x.posicao = x.posicao - 1
        if x.posicao == id:
            atendimento = x

    if atendimento == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Erro": "Cliente não encontrado neste posição da fila"}

    lista.remove(atendimento)

    return {"atendimento": atendimento}

# Preenchendo pessoas na fina
@app.get("/preenche") 
async def Preenche():
    atendimento = Atendimento(nome="Gustavo",prioridade="N", posicao= 1)
    lista.append(atendimento)
    
    atendimento = Atendimento(nome="Matheus", prioridade="N", posicao=  2)
    lista.append(atendimento)
    
    atendimento = Atendimento(nome="Lucas", prioridade="N", posicao=  3)
    lista.append(atendimento)
    
    atendimento = Atendimento(nome="José", prioridade="P", posicao=  4)
    lista.append(atendimento)

    atendimento = Atendimento(nome="Maria", prioridade="P", posicao=  5)
    lista.append(atendimento)

    atendimento = Atendimento(nome="Rodrigo", prioridade="N", posicao=  6)
    lista.append(atendimento)

    return {"fila": lista}