import traceback

from flask import Blueprint, request, jsonify, make_response
from app.modules.produto.dao import ProdutoDao
from app.modules.produto.modelo import Produto
from app.util.conexao import ConnectSingletonDB


app_produto = Blueprint('app_produto', __name__)
app_name = 'produto'
dao = ProdutoDao(database=ConnectSingletonDB())


@app_produto.route('/{}/'.format(app_name), methods=['GET'])
def get_produtos():
    produtos = dao.get_all()
    return make_response(jsonify(produtos), 200)


@app_produto.route('/{}/add/'.format(app_name), methods=['POST'])
def new_produtos():
    try:
        data = request.args.to_dict(flat=True)
        produto = Produto(nome_produto=data.get('nome_produto'),
                          marca=data.get('marca'),
                          valor_produto=data.get('valor_produto'))
        produto = dao.save(produto)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return make_response(
            {
                'error': True,
                'message': str(e)
            }, 400)
    return make_response({'codigo_produto': produto.codigo_produto}, 201)


@app_produto.route('/{}/<int:codigo_produto>/'.format(app_name), methods=['PUT'])
def update_produtos(codigo_produto):
    data = request.args.to_dict(flat=True)
    produto = dao.get_by_codigo_produto(codigo_produto)
    if not produto:
        return make_response({'error': '{} não existe'.format(app_name)}, 404)
    dao.edit(codigo_produto, data)
    produto = dao.get_by_codigo_produto(codigo_produto)
    return make_response(produto, 200)


@app_produto.route('/{}/delete/<int:codigo_produto>/'.format(app_name), methods=['DELETE'])
def delete_produtos(codigo_produto):
    try:
        dao.delete_by_codigo_produto(codigo_produto)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return make_response(
            {
                'error': True,
                'message': str(e)
            }, 400)
    return make_response({'codigo excluído': codigo_produto}, 201)


@app_produto.route('/{}/<int:codigo_produto>/'.format(app_name), methods=['GET'])
def get_produtos_codigo(codigo_produto):
    produto = dao.get_by_codigo_produto(codigo_produto)
    if not produto:
        return make_response({'error': '{} não existe'.format(app_name)}, 404)
    return make_response(produto, 201)
