TABLE_SQL_TABLE = 'USUARIOS'
_SCRIPT_SQL_INSERT = 'INSERT INTO USUARIOS (nome, email, senha) values (%s, %s, %s) returning matricula'
_SCRIPT_SQL_UPDATE_BY_MATRICULA = 'UPDATE USUARIOS SET {} WHERE MATRICULA={}'
_SCRIPT_SQL_SELECT_BY_MATRICULA = "SELECT * FROM USUARIOS WHERE matricula={}"
_SCRIPT_SQL_SELECT = 'SELECT * FROM USUARIOS'
_SCRIPT_SQL_DELETE_BY_MATRICULA = "DELETE FROM USUARIOS WHERE MATRICULA={}"


class UsuarioDao:
    def __init__(self, database):
        self.database = database

    def save(self, usuario):
        cursor = self.database.connect.cursor()
        cursor.execute(_SCRIPT_SQL_INSERT, usuario.get_values_save())
        matricula = cursor.fetchone()[0]
        self.database.connect.commit()
        cursor.close()
        usuario.set_matricula(matricula)
        return usuario

    def edit(self, matricula, data_usuario):
        cursor = self.database.connect.cursor()
        str = []
        for key in data_usuario.keys():
            str.append('{}=%s'.format(key))
        cursor.execute(_SCRIPT_SQL_UPDATE_BY_MATRICULA.format(','.join(str), matricula), list(data_usuario.values()))
        self.database.connect.commit()
        cursor.close()
        return True

    def get_all_usuarios_matricula(self, script):
        usuarios = []
        cursor = self.database.connect.cursor()
        cursor.execute(script)
        columns_name = [column[0] for column in cursor.description]
        usuario_cursor = cursor.fetchone()
        while usuario_cursor:
            usuario = dict(zip(columns_name, usuario_cursor))
            usuario_cursor = cursor.fetchone()
            usuarios.append(usuario)
        cursor.close()
        print(usuarios)
        return usuarios

    def get_by_matricula(self, matricula):
        usuarios = self.get_all_usuarios_matricula(_SCRIPT_SQL_SELECT_BY_MATRICULA.format(matricula))
        if usuarios:
            return usuarios[0]
        return None

    def get_all(self):
        usuarios = self.get_all_usuarios_matricula(_SCRIPT_SQL_SELECT)
        return usuarios

    def delete_by_matricula(self, matricula):
        cursor = self.database.connect.cursor()
        cursor.execute(_SCRIPT_SQL_DELETE_BY_MATRICULA.format(matricula))
        self.database.connect.commit()
        cursor.close()
