import zmq
from datetime import datetime

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://broker:5556")

tarefas = {}
proximo_id = 1


def criar_tarefa(nome, descricao, concluir_em):
    global proximo_id
    identificador = proximo_id
    tarefas[identificador] = {
        "nome": nome,
        "descricao": descricao,
        "criada_em": datetime.now().isoformat(timespec="seconds"),
        "concluir_em": concluir_em,
    }
    proximo_id += 1
    return f"Tarefa criada com o ID {identificador}."


def listar_tarefas():
    if not tarefas:
        return "VAZIA"

    return "\n".join(
        f"{identificador};{tarefa['nome']};{tarefa['descricao']};"
        f"{tarefa['criada_em']};{tarefa['concluir_em']}"
        for identificador, tarefa in tarefas.items()
    )


def excluir_tarefa(identificador):
    try:
        identificador = int(identificador)
    except ValueError:
        return "ID inválido."

    if tarefas.pop(identificador, None) is None:
        return "Tarefa não encontrada."
    return "Tarefa excluída."


def processar_solicitacao(solicitacao):
    partes = solicitacao.split(";")
    acao = partes[0].lower()

    if acao == "criar" and len(partes) == 4:
        return criar_tarefa(partes[1], partes[2], partes[3])
    if acao == "listar" and len(partes) == 1:
        return listar_tarefas()
    if acao == "excluir" and len(partes) == 2:
        return excluir_tarefa(partes[1])
    return "Solicitação inválida."


while True:
    solicitacao = socket.recv_string()
    resposta = processar_solicitacao(solicitacao)
    socket.send_string(resposta)

