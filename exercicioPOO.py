"""
Exercício com Abstração, Herança, Encapsulamento e Polimorfismo
Criar um sistema bancário (extremamente simples) que tem clientes, contas e
um banco. A ideia é que o cliente tenha uma conta (poupança ou corrente) e que
possa sacar/depositar nessa conta. Contas corrente tem um limite extra.
Conta (ABC)
    ContaCorrente
    ContaPoupanca
Pessoa (ABC)
    Cliente
        Clente -> Conta
Banco
    Banco -> Cliente
    Banco -> Conta
Dicas:
Criar classe Cliente que herda da classe Pessoa (Herança)
    Pessoa tem nome e idade (com getters)
    Cliente TEM conta (Agregação da classe ContaCorrente ou ContaPoupanca)
Criar classes ContaPoupanca e ContaCorrente que herdam de Conta
    ContaCorrente deve ter um limite extra
    Contas têm agência, número da conta e saldo
    Contas devem ter método para depósito
    Conta (super classe) deve ter o método sacar abstrato (Abstração e
    polimorfismo - as subclasses que implementam o método sacar)
Criar classe Banco para AGREGAR classes de clientes e de contas (Agregação)
Banco será responsável autenticar o cliente e as contas da seguinte maneira:
    Banco tem contas e clentes (Agregação)
    * Checar se a agência é daquele banco
    * Checar se o cliente é daquele banco
    * Checar se a conta é daquele banco
Só será possível sacar se passar na autenticação do banco (descrita acima)
Banco autentica por um método.
"""
from abc import abstractclassmethod, abstractmethod, ABC

class Conta(ABC):   
    def __init__(self, agencia, conta, saldo):
        self._agencia = agencia
        self._conta = conta
        self._saldo = saldo

    @abstractmethod
    def sacar(self, valor):...

    def depositar(self, valor):
        self._saldo += valor
        self.detalhes(f'(DEPÓSITO {valor}R$)')

    def detalhes(self, msg=''):
        print(f'O seu saldo é {self._saldo:.2f} R$ {msg}')

class ContaPoupanca(Conta):
    def sacar(self, valor):
        valor_pos_saque = self._saldo - valor

        if valor_pos_saque >= 0:
            self._saldo -= valor
            self.detalhes(f'(SAQUE {valor} R$)')
            return self._saldo

        print('Não foi possível sacar esse valor')
        self.detalhes(f'(Saque NEGADO {valor} R$)')
    
    def __repr__(self):
        class_name = self.__class__.__name__
        attrs = f'({self._agencia!r}, {self._conta!r}, {self._saldo!r})'
        return f'{class_name} {attrs}'

class ContaCorrente(Conta):
    def __init__(self, agencia, conta, saldo = 0, limite = 0):
        super().__init__(agencia, conta, saldo)
        self.limite = limite

    def sacar(self, valor):
        valor_pos_saque = self._saldo - valor
        limite_maximo = -self.limite

        if valor_pos_saque >= limite_maximo:
            self._saldo -= valor
            self.detalhes(f'(SAQUE {valor} R$)')
            return self._saldo

        print('Não foi possível sacar esse valor')
        print(f'Seu limite é de {self.limite:.2f}')
        self.detalhes(f'(Saque NEGADO {valor} R$)')
    def __repr__(self):
        class_name = self.__class__.__name__
        attrs = f'({self._agencia!r}, {self._conta!r}, {self._saldo!r}, {self.limite!r})'
        return f'{class_name} {attrs}'





    
    


class Pessoa:
    def __init__(self, nome, idade):
        self._nome = nome
        self._idade = idade

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome (self, valor):
        self._nome = valor

    @property
    def idade(self):
        return self._idade
    
    @idade.setter
    def idade(self,valor):
        self._idade = valor

    def __repr__(self):
        class_name = self.__class__.__name__
        attrs = f'({self._nome!r}, {self._idade!r})'
        return f'{class_name} {attrs}'


        






class Cliente(Pessoa):
    def __init__(self, nome, idade):
        super().__init__(nome, idade)
        self.conta = None


class Banco:
    def __init__(self, agencias: list[int] | None= None, clientes:list[Pessoa] | None = None, contas:list[Conta] | None = None):
        self.agencias = agencias or []
        self.clientes = clientes or []
        self.contas = contas or []
    def _checa_agencia(self, conta):
        if conta._agencia in self.agencias:
            return True
        return False


 

    def _checa_cliente(self, cliente):
        if cliente in self.clientes:
            return True
        return False

    def _checa_conta(self, conta):
        if conta in self.contas:
            return True
        return False
    
    def _checa_se_conta_e_do_cliente(self, cliente, conta):
        if conta is cliente.conta:
            print('_checa_se_conta_e_do_cliente', True)
            return True
        print('_checa_se_conta_e_do_cliente', False)
        return False

    def autenticar(self, cliente: Pessoa, conta: Conta):
        return self._checa_agencia(conta) and \
            self._checa_cliente(cliente) and \
            self._checa_conta(conta)
            
    
    def __repr__(self):
        class_name = self.__class__.__name__
        attrs = f'({self.agencias!r}, {self.clientes!r}, {self.contas!r})'
        return f'{class_name} {attrs}'





cliente_1 = Cliente('Jão', 22)
print(cliente_1)


cliente_1_conta = ContaCorrente(111,222,0,100)
print(cliente_1_conta)

cliente_2 = Cliente('Maria', 33)
cliente_2_conta = ContaPoupanca(222,333,0)

banco = Banco()

banco.clientes.extend([cliente_1,cliente_2])
banco.contas.extend([cliente_1_conta, cliente_2_conta])
banco.agencias.extend([111,222])

print(banco.autenticar(cliente_1,cliente_2_conta))

print(banco)