import traceback

from flask import Blueprint, request, jsonify, make_response
from app.modules.usuario.dao import UsuarioDao
from app.modules.usuario.modelo import Usuario
from app.util.conexao import ConnectSingletonDB


app_usuario = Blueprint('app_usuario', __name__)
app_name = 'usuario'
dao = UsuarioDao(database=ConnectSingletonDB())


@app_usuario.route('/{}/'.format(app_name), methods=['GET'])
def get_usuarios():
    usuarios = dao.get_all()
    return make_response(jsonify(usuarios), 200)


@app_usuario.route('/{}/add/'.format(app_name), methods=['POST'])
def new_usuarios():
    try:
        data = request.args.to_dict(flat=True)
        usuario = Usuario(nome=data.get('nome'),
                          email=data.get('email'),
                          senha=data.get('senha'))
        usuario = dao.save(usuario)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return make_response(
            {
                'error': True,
                'message': str(e)
            }, 400)
    return make_response({'matricula': usuario.matricula}, 201)


@app_usuario.route('/{}/<int:matricula>/'.format(app_name), methods=['PUT'])
def update_usuarios(matricula):
    data = request.args.to_dict(flat=True)
    usuario = dao.get_by_matricula(matricula)
    if not usuario:
        return make_response({'error': '{} não existe'.format(app_name)}, 404)
    dao.edit(matricula, data)
    usuario = dao.get_by_matricula(matricula)
    return make_response(usuario, 200)


@app_usuario.route('/{}/delete/<int:matricula>/'.format(app_name), methods=['DELETE'])
def delete_usuarios(matricula):
    try:
        dao.delete_by_matricula(matricula)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return make_response(
            {
                'error': True,
                'message': str(e)
            }, 400)
    return make_response({'matricula excluída': matricula}, 201)


@app_usuario.route('/{}/<int:matricula>/'.format(app_name), methods=['GET'])
def get_usuarios_matricula(matricula):
    usuario = dao.get_by_matricula(matricula)
    if not usuario:
        return make_response({'error': '{} não existe'.format(app_name)}, 404)
    return make_response(usuario, 201)
