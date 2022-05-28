class Usuario:

    def __init__(self, nome, email, senha, matricula=None):
        self.matricula = matricula
        self.nome = nome
        self.email = email
        self.senha = senha

    def set_matricula(self, matricula):
        self.matricula = matricula

    def __str__(self):
        return 'Nome: {} - Email: {} - Senha: {}'. format(self.nome, self.email, self.senha)

    def get_values_save(self):
        return [self.nome, self.email, self.senha]
