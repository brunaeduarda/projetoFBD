import traceback

from flask import Blueprint, request, jsonify, make_response
from app.modules.venda.dao import VendaDao
from app.modules.venda.modelo import Venda
from app.util.conexao import ConnectSingletonDB


app_venda = Blueprint('app_venda', __name__)
app_name = 'venda'
dao = VendaDao(database=ConnectSingletonDB())


@app_venda.route('/{}/'.format(app_name), methods=['GET'])
def get_vendas():
    vendas = dao.get_all()
    return make_response(jsonify(vendas), 200)


@app_venda.route('/{}/add/'.format(app_name), methods=['POST'])
def new_vendas():
    try:
        data = request.form.to_dict(flat=True)
        venda = Venda(valor_venda=data.get('valor_venda'))
        venda = dao.save(venda)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return make_response(
            {
                'error': True,
                'message': str(e)
            }, 400)
    return make_response({'codigo_venda': venda.codigo_venda}, 201)


@app_venda.route('/{}/<int:codigo_venda>/'.format(app_name), methods=['PUT'])
def update_vendas(codigo_venda):
    data = request.form.to_dict(flat=True)
    venda = dao.get_by_codigo_venda(codigo_venda)
    if not venda:
        return make_response({'error': '{} não existe'.format(app_name)}, 404)
    dao.edit(codigo_venda, data)
    venda = dao.get_by_codigo_venda(codigo_venda)
    return make_response(venda, 200)


@app_venda.route('/{}/<int:codigo_venda>/'.format(app_name), methods=['GET'])
def get_vendas_codigo(codigo_venda):
    venda = dao.get_by_codigo_venda(codigo_venda)
    if not venda:
        return make_response({'error': '{} não existe'.format(app_name)}, 404)
    return make_response(venda, 201)
