import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://broker:5555")

def enviar(mensagem):
    socket.send_string(mensagem)
    return socket.recv_string()


def mostrar_tarefas(resposta):
    if resposta == "VAZIA":
        print("Nenhuma tarefa cadastrada.")
        return

    print("\nTarefas:")
    for tarefa in resposta.splitlines():
        identificador, nome, descricao, criada_em, concluir_em = tarefa.split(";", 4)
        print(f"[{identificador}] {nome}")
        print(f"  Descrição: {descricao}")
        print(f"  Criada em: {criada_em}")
        print(f"  Concluir até: {concluir_em}")


def criar_tarefa():
    nome = input("Nome: ").strip()
    descricao = input("Descrição: ").strip()
    concluir_em = input("Data para conclusão (AAAA-MM-DD): ").strip()

    if not nome or not descricao or not concluir_em:
        print("Todos os campos são obrigatórios.")
        return

    resposta = enviar(f"criar;{nome};{descricao};{concluir_em}")
    print(resposta)


def listar_tarefas():
    resposta = enviar("listar")
    mostrar_tarefas(resposta)


def excluir_tarefa():
    identificador = input("ID da tarefa: ").strip()

    if not identificador:
        print("Informe o ID da tarefa.")
        return

    print(enviar(f"excluir;{identificador}"))


while True:
    print("\nGerenciador de tarefas")
    print("1. Criar tarefa")
    print("2. Listar tarefas")
    print("3. Excluir tarefa")
    print("0. Sair")
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        criar_tarefa()
    elif opcao == "2":
        listar_tarefas()
    elif opcao == "3":
        excluir_tarefa()
    elif opcao == "0":
        break
    else:
        print("Opção inválida.")
