NAME_TABLE_SQL = "VENDA"
_SCRIPT_SQL_INSERT = 'INSERT INTO VENDAS (valor_venda) values (%s) returning codigo_venda'
_SCRIPT_SQL_UPDATE_BY_CODIGO_VENDA = 'UPDATE VENDAS SET {} WHERE CODIGO_VENDA={}'
_SCRIPT_SQL_SELECT_BY_CODIGO_VENDA = "SELECT * FROM VENDAS WHERE codigo_venda={}"
_SCRIPT_SQL_SELECT = 'SELECT * FROM VENDAS'


class VendaDao:
    def __init__(self, database):
        self.database = database

    def save(self, venda):
        cursor = self.database.connect.cursor()
        cursor.execute(_SCRIPT_SQL_INSERT, venda.get_values_save())
        codigo_venda = cursor.fetchone()[0]
        self.database.connect.commit()
        cursor.close()
        venda.set_codigo_venda(codigo_venda)
        return venda

    def edit(self, codigo_venda, data_venda):
        cursor = self.database.connect.cursor()
        str = []
        for key in data_venda.keys():
            str.append('{}=%s'.format(key))
        cursor.execute(_SCRIPT_SQL_UPDATE_BY_CODIGO_VENDA.format(','.join(str), codigo_venda),
                       list(data_venda.values()))
        self.database.connect.commit()
        cursor.close()
        return True

    def get_all_vendas_codigo_venda(self, script):
        vendas = []
        cursor = self.database.connect.cursor()
        cursor.execute(script)
        columns_name = [column[0] for column in cursor.description]
        venda_cursor = cursor.fetchone()
        while venda_cursor:
            venda = dict(zip(columns_name, venda_cursor))
            venda_cursor = cursor.fetchone()
            vendas.append(venda)
        cursor.close()
        return vendas

    def get_by_codigo_venda(self, codigo_venda):
        vendas = self.get_all_vendas_codigo_venda(_SCRIPT_SQL_SELECT_BY_CODIGO_VENDA.format(codigo_venda))
        if vendas:
            return vendas[0]
        return None

    def get_all(self):
        vendas = self.get_all_vendas_codigo_venda(_SCRIPT_SQL_SELECT)
        return vendas
