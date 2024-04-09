saldo = 0.0
extrato = ""
operacoes_saque = 0
LIMITE_OPERACOES_SAQUE = 3

def menu():
  print("\n1. Ver saldo")
  print("2. Realizar depósito")
  print("3. Realizar saque")
  print("4. Ver extrato")
  print("5. Sair\n")

def ver_saldo():
  print("\nSeu saldo é de: R$ ", saldo)

def depositar():
  global saldo
  global extrato
  deposito = float(input("\nDigite o valor para depósito: "))
  if deposito <= 0:
    print("O valor do depósito deve ser maior que zero!")
  else:
    saldo += deposito
    extrato += f"- Depósito de R$ {deposito:.2f}\n"
    print("Depósito realizado com sucesso!")

def sacar():
  global saldo
  global operacoes_saque
  global extrato
  if operacoes_saque == LIMITE_OPERACOES_SAQUE:
    print("Limite de saques excedido!")
    return
  saque = float(input("\nDigite o valor para saque: "))
  if saque <= 0:
    print("O valor do saque deve ser maior que zero!")
  elif saque <= saldo and saque <= 500:
    saldo -= saque
    extrato += f"- Saque de R$ {saque:.2f}\n"
    operacoes_saque += 1
    print("Saque realizado com sucesso!")
  else:
    print("Saldo insuficiente para este valor de saque!")
  
def realizar_extrato():
  global extrato
  if (extrato != ""):
    print(extrato)
    print("============")
    print("Saldo final: R$ ", saldo)
  else:
    print("Nenhuma operação registrada!")

while True:
  menu()
  opcao = int(input("Digite uma opção > "))

  if opcao == 1:
    ver_saldo()
  elif opcao == 2:
    depositar()
  elif opcao == 3:
    sacar()
  elif opcao == 4:
    realizar_extrato()
  elif opcao == 5:
    break
  else:
    print("Opção inválida!")