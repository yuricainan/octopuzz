# Sistema Financeiro Simples

# Lista de transações, onde cada transação será um dicionário {'tipo': 'entrada'/'saída', 'valor': float}
transacoes = []

# Função para adicionar uma transação
def adicionar_transacao(tipo, valor):
    if tipo not in ['entrada', 'saída']:
        print("Tipo inválido! Use 'entrada' ou 'saída'.")
        return
    
    if valor <= 0:
        print("O valor deve ser positivo.")
        return
    
    transacoes.append({'tipo': tipo, 'valor': valor})
    print(f"Transação de {tipo} de R${valor:.2f} adicionada com sucesso!")

# Função para exibir todas as transações
def exibir_transacoes():
    if not transacoes:
        print("Nenhuma transação registrada.")
        return
    
    print("\nTransações registradas:")
    for idx, transacao in enumerate(transacoes, start=1):
        print(f"{idx}. {transacao['tipo'].capitalize()}: R${transacao['valor']:.2f}")
    print()

# Função para calcular o saldo atual
def calcular_saldo():
    saldo = 0
    for transacao in transacoes:
        if transacao['tipo'] == 'entrada':
            saldo += transacao['valor']
        elif transacao['tipo'] == 'saída':
            saldo -= transacao['valor']
    
    return saldo

# Menu principal
def menu():
    while True:
        print("\nSistema Financeiro")
        print("1. Adicionar Entrada")
        print("2. Adicionar Saída")
        print("3. Exibir Transações")
        print("4. Exibir Saldo Atual")
        print("5. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            valor = float(input("Digite o valor da entrada: R$"))
            adicionar_transacao('entrada', valor)
        elif escolha == '2':
            valor = float(input("Digite o valor da saída: R$"))
            adicionar_transacao('saída', valor)
        elif escolha == '3':
            exibir_transacoes()
        elif escolha == '4':
            saldo = calcular_saldo()
            print(f"Saldo atual: R${saldo:.2f}")
        elif escolha == '5':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Iniciar o sistema
if __name__ == "__main__":
    menu()
