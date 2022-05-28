from flask import Flask

from app.modules.usuario.controller import app_usuario
from app.modules.produto.controller import app_produto
from app.modules.venda.controller import app_venda

app = Flask(__name__)

app.register_blueprint(app_usuario)
app.register_blueprint(app_produto)
app.register_blueprint(app_venda)


if __name__ == '__main__':
    app.run(debug=True)
