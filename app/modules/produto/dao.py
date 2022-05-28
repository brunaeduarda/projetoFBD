NAME_TABLE_SQL = "PRODUTO"
_SCRIPT_SQL_INSERT = 'INSERT INTO PRODUTOS (marca, nome_produto, valor_produto) values (%s, %s, %s) ' \
                     'returning codigo_produto'
_SCRIPT_SQL_UPDATE_BY_CODIGO_PRODUTO = 'UPDATE PRODUTOS SET {} WHERE CODIGO_PRODUTO={}'
_SCRIPT_SQL_SELECT_BY_CODIGO_PRODUTO = "SELECT * FROM PRODUTOS WHERE codigo_produto={}"
_SCRIPT_SQL_SELECT = 'SELECT * FROM PRODUTOS'
_SCRIPT_SQL_DELETE_BY_CODIGO_PRODUTO = "DELETE FROM PRODUTOS WHERE CODIGO_PRODUTO={}"


class ProdutoDao:
    def __init__(self, database):
        self.database = database

    def save(self, produto):
        cursor = self.database.connect.cursor()
        cursor.execute(_SCRIPT_SQL_INSERT, produto.get_values_save())
        codigo_produto = cursor.fetchone()[0]
        self.database.connect.commit()
        cursor.close()
        produto.set_codigo_produto(codigo_produto)
        return produto

    def edit(self, codigo_produto, data_produto):
        cursor = self.database.connect.cursor()
        str = []
        for key in data_produto.keys():
            str.append('{}=%s'.format(key))
        cursor.execute(_SCRIPT_SQL_UPDATE_BY_CODIGO_PRODUTO.format(','.join(str), codigo_produto),
                       list(data_produto.values()))
        self.database.connect.commit()
        cursor.close()
        return True

    def get_all_produtos_codigo_produto(self, script):
        produtos = []
        cursor = self.database.connect.cursor()
        cursor.execute(script)
        columns_name = [column[0] for column in cursor.description]
        produto_cursor = cursor.fetchone()
        while produto_cursor:
            produto = dict(zip(columns_name, produto_cursor))
            produto_cursor = cursor.fetchone()
            produtos.append(produto)
        cursor.close()
        return produtos

    def get_by_codigo_produto(self, codigo_produto):
        produtos = self.get_all_produtos_codigo_produto(_SCRIPT_SQL_SELECT_BY_CODIGO_PRODUTO.format(codigo_produto))
        if produtos:
            return produtos[0]
        return None

    def get_all(self):
        produtos = self.get_all_produtos_codigo_produto(_SCRIPT_SQL_SELECT)
        return produtos

    def delete_by_codigo_produto(self, codigo_produto):
        cursor = self.database.connect.cursor()
        cursor.execute(_SCRIPT_SQL_DELETE_BY_CODIGO_PRODUTO.format(codigo_produto))
        self.database.connect.commit()
        cursor.close()
