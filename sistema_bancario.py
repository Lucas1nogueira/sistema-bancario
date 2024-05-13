from datetime import datetime

usuarios = []
contas = []
usuario_logado = False
usuario_atual = {}
LIMITE_OPERACOES = 10

def decorador(funcao):
  def add_info(*args, **kwargs):
    resultado = funcao(*args, **kwargs)
    print(f"\n{datetime.now()}: {funcao.__name__}")
    print(f"\n")
    return resultado
  return add_info

def verificar_existencia_usuario(cpf):
  usuario = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
  if (usuario):
    return usuario[0]
  else:
    return None

def criar_usuario():
  global usuarios

  cpf = input("Digite o CPF: ")
  usuario = verificar_existencia_usuario(cpf)

  if usuario is not None:
    print("CPF já cadastrado!")
    return

  nome = input("Digite o nome do usuário: ")
  data_nascimento = input("Informe a data de nascimento (DD-MM-AAAA): ")
  endereco = input("Informe o endereço (logradouro, número - bairro - cidade / sigla estado): ")
  senha = input("Digite uma senha: ")

  usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereço": endereco, "senha": senha})
  print("\nUsuário criado com sucesso!")

def criar_conta(usuario):
  global contas
  
  numero = len(contas) + 1
  contas.append({"agencia": "0001", "numero": numero, "cpf": usuario["cpf"], "usuario": usuario, "saldo": 0, "extrato": []})
  
  print("\nConta criada com sucesso!")
  print("Informações da nova conta:")
  print("Agência: 0001")
  print(f"Número: {numero}")

def entrar():
  global usuarios
  global usuario_logado
  global usuario_atual

  cpf = input("Informe seu CPF: ")

  usuario = verificar_existencia_usuario(cpf)

  if usuario is None:
    print("Usuário não encontrado!")
    return
  
  senha = input("Digite sua senha: ")

  if usuario["senha"] == senha:
    usuario_logado = True
    usuario_atual = usuario
    print("\nLogin efetuado com sucesso!")
  else:
    print("\nSenha incorreta!")

class ContaIterador:
  def __init__(self, contas: list[dict]):
    self.contas = contas
    self.contador = 0
  def __iter__(self):
    return self
  def __next__(self):
    try:
      conta = self.contas[self.contador]
      self.contador += 1
      return conta
    except IndexError:
      raise StopIteration

def menu_deslogado():
  global usuario_logado
  global contas
  while usuario_logado == False:
    print("\n=== Seja bem-vindo! ===")
    print("0. Exibir contas cadastradas")
    print("1. Criar usuário")
    print("2. Entrar")
    print("3. Sair")
    opcao = int(input("\nDigite uma opção > "))
    if opcao == 0:
      if contas.__len__() == 0:
        print("\nNenhuma conta encontrada!")
      else:
        for i in ContaIterador(contas):
          print(f"\n{i.get('agencia')}.{i.get('numero')}\nCPF: {i.get('cpf')}\nSaldo: {i.get('saldo')}\n")
    elif opcao == 1:
      criar_usuario()
    elif opcao == 2:
      entrar()
    elif opcao == 3:
      exit()
    else:
      print("Opção inválida!")

def menu_logado():
  global usuario_logado
  global usuarios
  global contas
  global usuario_atual
  global extrato
  conta_selecionada = False
  numero_conta = None
  operacoes = 0

  while usuario_logado == True:
    contas_usuario = [conta for conta in contas if conta["usuario"] == usuario_atual]
    
    print("\n=== Seja bem-vindo, ", usuario_atual["nome"], " ===")
    print("\nPor favor, escolha uma opção abaixo:")
    print("1. Criar conta")
    print("2. Acessar conta(s)")
    print("3. Sair")

    opcao = int(input("\nDigite uma opção > "))

    if opcao == 3:
      usuario_logado = False
      usuario_atual = {}
      return
    
    if opcao == 2:
      if len(contas_usuario) == 0:
        print("\nNenhuma conta cadastrada para este usuário!")
      else:
        print("\nContas cadastradas: ")
        for conta in contas_usuario:
          print("Ag.: ", conta["agencia"], "Número: ", conta["numero"])
        numero = input("\nDigite o número da conta desejada ou enter para retornar > ")
        if numero is not None and numero != "":
          if int(numero) in [conta["numero"] for conta in contas_usuario]:
            conta_selecionada = True
            numero_conta = int(numero)
          else:
            print("Número inválido!")
    
    elif opcao == 1:
      criar_conta(usuario_atual)
    else:
      print("Opção inválida!")
    
    while conta_selecionada == True:
      print("\n=== CONTA ", numero_conta, " ===")
      print("\n1. Ver saldo")
      print("2. Realizar depósito")
      print("3. Realizar saque")
      print("4. Ver extrato")
      print("5. Retornar\n")
      opcao = int(input("Digite uma opção > "))
      if opcao == 1:
        ver_saldo(numero_conta)
      elif opcao == 2:
        if operacoes == LIMITE_OPERACOES:
          print("Limite de operações excedido!")
        else:
          valor_deposito = float(input("\nDigite o valor para depósito: "))
          novo_saldo = depositar(numero_conta, valor_deposito)
          if novo_saldo is not None:
            print("Saldo atual: R$ ", novo_saldo)
            operacoes += 1
      elif opcao == 3:
        if operacoes == LIMITE_OPERACOES:
          print("Limite de operações excedido!")
        else:
          valor_saque = float(input("\nDigite o valor para saque: "))
          novo_saldo = sacar(numero_conta=numero_conta, valor=valor_saque)
          if novo_saldo is not None:
            print("Saldo atual: R$ ", novo_saldo)
            operacoes += 1
      elif opcao == 4:
        for conta in contas:
          if conta["numero"] == numero_conta:
            saldo = conta["saldo"]
            extrato = conta["extrato"]
        tirar_extrato(saldo, extrato=extrato)
      elif opcao == 5:
        conta_selecionada = False
        numero_conta = None
        break
      else:
        print("Opção inválida!")

@decorador
def ver_saldo(numero_conta):
  global contas

  for conta in contas:
    if conta["numero"] == numero_conta:
      saldo = conta["saldo"]

  print("\nSeu saldo é de: R$ ", saldo)

@decorador
def depositar(numero_conta, valor):
  global contas

  if valor <= 0:
    print("O valor do depósito deve ser maior que zero!")
    return None
  
  for conta in contas:
    if conta["numero"] == numero_conta:
      conta["saldo"] += valor
      conta["extrato"].append({"operacao": "deposito", "valor": valor, "data": datetime.now()})
      print("Depósito realizado com sucesso!")
      return conta["saldo"]

@decorador
def sacar(numero_conta=None, valor=0):
  global contas

  if valor <= 0:
    print("O valor do saque deve ser maior que zero!")
    return None
  
  if valor >= 500:
    print("O valor excede o limite de saque disponível!")
    return None

  for conta in contas:
    if conta["numero"] == numero_conta:
      saldo = conta["saldo"]
      if valor <= saldo:
        conta["saldo"] = conta["saldo"] - valor
        conta["extrato"].append({"operacao": "saque", "valor": valor, "data": datetime.now()})
        print("Saque realizado com sucesso!")
        return conta["saldo"]
      else:
        print("Saldo insuficiente!")
        return None

def gerador_extrato(extrato: list[dict], filtro):
  for operacao in extrato:
    if filtro == 1:
      yield operacao
    elif filtro == 2:
      if operacao["operacao"] == "deposito":
        yield operacao
    elif filtro == 3:
      if operacao["operacao"] == "saque":
        yield operacao

@decorador
def tirar_extrato(saldo, extrato=[]):
  if (extrato != []):
    print("\n1. Tudo")
    print("2. Depósitos")
    print("3. Saques")
    opcao = int(input("\nDigite uma opção > "))
    if opcao < 1 or opcao > 3:
      print("\nOpção inválida!")
      return
    print("\nResultado:")
    for op in gerador_extrato(extrato, opcao):
      print(f"{op['data']}: {op['operacao']} de R$ {op['valor']}")
  else:
    print("Nenhuma operação registrada!")

while True:
  if not usuario_logado:
    menu_deslogado()
  else:
    menu_logado()