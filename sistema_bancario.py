from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
  def __init__(self, endereco):
    self.endereco = endereco
    self.contas = []

  def realizar_transacao(self, conta, transacao):
    transacao.registrar(conta)
  
  def adicionar_conta(self, conta):
    self.contas.append(conta)

class PessoaFisica(Cliente):
  def __init__(self, nome, data_nascimento, cpf, endereco):
    super().__init__(endereco)
    self.nome = nome
    self.data_nascimento = data_nascimento
    self.cpf = cpf

class Conta:
  def __init__(self, numero, cliente):
    self._saldo = 0
    self._numero = numero
    self._agencia = "0001"
    self._cliente = cliente
    self._historico = Historico()
  
  @classmethod
  def nova_conta(cls, numero, cliente):
    return cls(numero, cliente)
  
  @property
  def agencia(self):
    return self._agencia
  
  @property
  def numero(self):
    return self._numero
  
  @property
  def saldo(self):
    return self._saldo
  
  @property
  def cliente(self):
    return self._cliente
  
  @property
  def historico(self):
    return self._historico
  
  def sacar(self, valor):
    if valor <= 0:
      print("O valor do saque deve ser maior que zero!")
      return False
    elif valor > self._saldo:
      print("Saldo insuficiente!")
    else:
      self._saldo -= valor
      print("Saque realizado com sucesso!")
      return True
  
  def depositar(self, valor):
    if valor <= 0:
      print("O valor do depósito deve ser maior que zero!")
      return False
    else:
      self._saldo += valor
      print("Depósito realizado com sucesso!")
      return True

class ContaCorrente(Conta):
  def __init__(self, numero, cliente, limite=500, limite_saques=3):
    super().__init__(numero, cliente)
    self.limite = limite
    self.limite_saques = limite_saques
  
  def sacar(self, valor):
    numero_saques = 0
    for transacao in self.historico.transacoes:
      if transacao["tipo"] == Saque.__name__:
        numero_saques +=1
    if numero_saques >= self.limite_saques:
      print("Limite de saques excedido!")
      return False
    elif valor > self.limite:
      print("Saldo insuficiente!")
      return False
    else:
      return super().sacar(valor)
  
  def __str__(self):
    return f"Agência: {self.agencia}\nNúmero: {self.numero}\nTitular: {self.cliente.nome}"
  
class Historico:
  def __init__(self):
    self._transacoes = []

  @property
  def transacoes(self):
    return self._transacoes
  
  def adicionar_transacao(self, transacao):
    self._transacoes.append(
      {
        "tipo":transacao.__class__.__name__,
        "valor": transacao.valor,
        "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
      }
    )

class Transacao(ABC):
  @property
  @abstractmethod
  def valor(self):
    pass

  @abstractmethod
  def registrar(self, conta):
    pass

class Saque(Transacao):
  def __init__(self, valor):
    self._valor = valor
  
  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta):
    if conta.sacar(self.valor):
      conta.historico.adicionar_transacao(self)
  
class Deposito(Transacao):
  def __init__(self, valor):
    self._valor = valor
  
  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta):
    if conta.depositar(self.valor):
      conta.historico.adicionar_transacao(self)

def menu():
  print("""\n=== MENU ===
  1. Depositar
  2. Sacar
  3. Extrato
  4. Criar conta
  5. Listar contas
  6. Novo usuário
  7. Sair
  """)
  return int(input("Digite a opção escolhida > "))

def main():
  clientes = []
  contas = []

  while True:
    opcao = menu()

    match opcao:
      case 1:
        depositar(clientes)
      case 2:
        sacar(clientes)
      case 3:
        exibir_extrato(clientes)
      case 4:
        criar_conta(contas, clientes, (len(contas) + 1))
      case 5:
        listar_contas(contas)
      case 6:
        criar_cliente(clientes)
      case 7:
        break

def filtrar_cliente(cpf, clientes):
  for cliente in clientes:
    if cliente.cpf == cpf:
      return cliente
  return None

def recuperar_conta_cliente(cliente):
  if not cliente.contas:
    print("Este cliente não possui contas!")
    return
  return cliente.contas[0]

def listar_contas(contas):
  for conta in contas:
    print("... " * 5)
    print(str(conta))

def depositar(clientes):
  cpf = input("Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\nCliente não encontrado!")
    return
  
  valor = float(input("Digite o valor do depósito: "))
  transacao = Deposito(valor)

  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return
  
  cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
  cpf = input("Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\nCliente não encontrado!")
    return
  
  valor = float(input("Digite o valor do saque: "))
  transacao = Saque(valor)

  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return
  
  cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
  cpf = input("Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\nCliente não encontrado!")
    return
  
  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return
  
  print("\n=== EXTRATO ===")
  transacoes = conta.historico.transacoes
  extrato = ""

  if not transacoes:
    extrato = "Não foram realizadas movimentações."
  else:
    for transacao in transacoes:
      extrato += f"\n{transacao['data']} : {transacao['tipo']} -> R$ {transacao['valor']}"
  
  print(extrato)
  print(f"\nSaldo: R$ {conta.saldo:.2f}")
  print("... ... ... ... ... ... ... ...")

def criar_cliente(clientes):
  cpf = input("Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if cliente:
    print("\nEsse CPF já está registrado!")
    return
  
  nome = input("Digite o nome do cliente: ")
  data_nascimento = input("Digite a data de nascimento do cliente: ")
  endereco = input("Digite o endereço do cliente: ")

  cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
  clientes.append(cliente)
  print("\nCliente criado com sucesso!")

def criar_conta(contas, clientes, numero_conta):
  cpf = input("Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\nCliente não encontrado!")
    return
  
  conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
  contas.append(conta)
  cliente.contas.append(conta)
  print("\nConta criada com sucesso!")

main()