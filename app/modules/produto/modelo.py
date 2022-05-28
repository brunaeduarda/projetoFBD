class Produto:

    def __init__(self, marca, nome_produto, valor_produto, codigo_produto=None):
        self.codigo_produto = codigo_produto
        self.marca = marca
        self.nome_produto = nome_produto
        self.valor_produto = valor_produto

    def set_codigo_produto(self, codigo_produto):
        self.codigo_produto = codigo_produto

    def __str__(self):
        return 'Marca: {} - Nome: {} - Valor: {}'. format(self.marca, self.nome_produto, self.valor_produto)

    def get_values_save(self):
        return [self.marca, self.nome_produto, self.valor_produto]
