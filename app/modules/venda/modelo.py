class Venda:

    def __init__(self, valor_venda, codigo_venda=None):
        self.codigo_venda = codigo_venda
        self.valor_venda = valor_venda

    def set_codigo_venda(self, codigo_venda):
        self.codigo_venda = codigo_venda

    def __str__(self):
        return 'Valor: {}'. format(self.valor_venda)

    def get_values_save(self):
        return [self.valor_venda]
