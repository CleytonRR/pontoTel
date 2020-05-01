from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flasgger import Swagger
from util.utils import get_price, valid_name
from model.models import User, Company, init_db
import asyncio

loop = asyncio.get_event_loop()
app = Flask(__name__)
CORS(app)
api = Api(app)
swagger = Swagger(app)

class Bovespa(Resource):
    def get(self):
        """
               Retorna o indice BOVESPA atual
               ---
               responses:
                 200:
                   description: Retorna o indice BOVESPA
                   schema:
                     id: User
                     properties:
                       BOVESPA:
                         type: string
                 500:
                   description: Se a quantidade de requisições na API ultrapassar o limite
                """
        try:
            price = loop.run_until_complete(get_price('^BVSP'))
            response = {
                'BOVESPA': price
            }
            return response
        except:
            return {'error': 'Erro interno'}, 500

class SearchName(Resource):
    def get(self, nome):
        """
               Retorna o indice baseado no nome da empresa
               ---
               parameters:
                 - name: nome
                   in: path
                   type: string
                   required: true
                   default: PETR4.SA
               responses:
                 200:
                   description: Retorna o indice baseado no nome da empresa
                   schema:
                     id: User
                     properties:
                       value:
                         type: string
                         default: valor
                 400:
                   description: Retorna error se o nome ou o simbolo forem inválidos
                """
        if valid_name(nome) == False:
            return {'error': 'Nome invalido'}, 400
        try:
            price = loop.run_until_complete(get_price(nome))
            response = {
                'value': price
            }
            return response
        except ValueError:
            return {'error': 'Simbolo invalido'}, 400

class UserMethods(Resource):
    def get(self, nome):
        """
               Retorna um usuário baseado no nome
               ---
               parameters:
                 - name: nome
                   in: path
                   type: string
                   required: true
               responses:
                 200:
                   description: Retorna um usuario baseado no nome
                   schema:
                     id: User
                     properties:
                       nome:
                         type: string
                 400:
                   description: Se o usuário não existir
        """
        try:
            user = User.query.filter_by(name=nome).first()
            response = {
                'nome': user.name
            }
        except AttributeError:
            response = {
                'error': 'User not found'
            }
            return response, 400
        return response

    def put(self, nome):
        """
               Atualiza um usuário
               ---
               parameters:
                 - name: nome
                   in: path
                   type: string
                   required: true

                 - name: nome
                   in: path
                   in: body
                   type: string
                   required: true
               responses:
                 200:
                   description: Atualiza o usuário
                   schema:
                     id: User
                     properties:
                       nome:
                         type: string
                 400:
                   description: Se o usuário não existir
        """
        try:
            user = User.query.filter_by(name=nome).first()
            dados = request.json
            if 'nome' in dados:
                user.name = dados['nome']
            user.save()
            response = {
                'id': user.id,
                'nome': user.name,
            }
        except AttributeError:
            response = {
                'error': 'User not found'
            }
            return response, 400
        return response

    def delete(self, nome):
        """
               Deleta um usuário
               ---
               parameters:
                 - name: nome
                   in: path
                   type: string
                   required: true
               responses:
                 204:
                   description: Retorna um usuario baseado no nome
                   schema:
                     id: User
                     properties:
                       message:
                         type: string
                 400:
                   description: Se o usuário não existir
        """
        try:
            user = User.query.filter_by(name=nome).first()
            user.delete()
            message = 'Usuario {} excluida com sucesso'.format(nome)
        except AttributeError:
            response = {
                'error': 'User not found'
            }
            return response, 400
        return {'message': message}, 204

class methodPostUser(Resource):
    def post(self):
        """
               Cria um novo usuário
               ---
               parameters:
                 - name: nome
                   in: body
                   type: string
                   required: true
                   default: { 'nome': 'any_name'}
               responses:
                 201:
                   description: Retorna um usuario baseado no nome
                   schema:
                     id: User
                     properties:
                       message:
                         type: string
                 400:
                   description: Se ocorrer qualquer erro
        """
        try:
            dados = request.json
            user = User(name=dados['nome'])
            user.save()
            response = {
                'id': user.id,
                'nome': user.name,
            }
        except:
            response = {
                'message': 'erro verifique os campos'
            }
            return response, 400
        return response, 201

class listCompanyByIdUser(Resource):
    def get(self, id):
        """
               Busca as empresas que o usuário escolheu baseado no id
               ---
               parameters:
                 - name: id
                   in: path
                   type: int
                   required: true
               responses:
                 200:
                   description: Retorna uma lista de empresas
                   schema:
                     id: User
                     properties:
                       message:
                         type: string
                 400:
                   description: Se o usuário não existir
        """
        try:
            companies = Company.query.filter_by(pessoa_id=id).all()
            response = [{'nome': i.name, 'symbol': i.symbol} for i in companies]
        except:
            response = {
                "message": "Erro ao buscar empresas"
            }
            return response, 400
        return response

class companyMethods(Resource):

    def get(self, id):
        """
                     Busca as empresas baseado no id
                     ---
                     parameters:
                       - name: id
                         in: path
                         type: integer
                         required: true
                     responses:
                       200:
                         description: Retorna uma empresa baseado no id
                         schema:
                           id: User
                           properties:
                             message:
                               type: string
                       400:
                         description: Se a empresa não existir
              """
        try:
            company = Company.query.filter_by(id=id).first()
            response = {
                "company": company.name,
                "symbol": company.symbol
            }
        except:
            response = {
                'error': 'Verique os dados'
            }
            return response, 400
        return response

    def delete(self, id):
        """
                     Deleta uma empresa baseado no id
                     ---
                     parameters:
                       - name: id
                         in: path
                         type: integer
                         required: true
                     responses:
                       204:
                         description: Mensagem de confirmação
                         schema:
                           id: User
                           properties:
                             message:
                               type: string
                       400:
                         description: Se a empresa não existir
              """
        try:
            company = Company.query.filter_by(id=id).first()
            company.delete()
            message = 'Empresa {} excluida com sucesso'.format(company.name)
        except:
            response = {
                'error': 'Verique os dados'
            }
            return response, 400
        return {'message': message}, 204

class methodPostCompany(Resource):
    def post(self):
        """
               Cria uma empresa associada a um usuário
               ---
               parameters:
                 - name: nome_empresa
                   in: body
                   type: string
                   required: true
                   default: { "name": "Petrobras", "symbol": "PETR4.SA", "user": "name_valid"}

               responses:
                 200:
                   description: Cria uma nova empresa associada a um user
                   schema:
                     id: User
                     properties:
                       nome:
                         type: string
                 400:
                   description: Se o usuário não existir ou se o nome da empresa for invalido.
        """
        try:
            dados = request.json
            if (not valid_name(dados['name']) or not valid_name(dados['symbol'])):
                response = {
                    "message": "Verifique o nome ou simbolo da empresa"
                }
                return response, 400
            user = User.query.filter_by(name=dados['user']).first()
            user.name
            price = loop.run_until_complete(get_price(dados['symbol']))
            company = Company(name=dados['name'], symbol= dados['symbol'], price=price, pessoa=user)
            company.save()
        except:
            response = {
                "message": "verifique os dados"
            }
            return response, 400
        response = {
            "id": company.id,
            "company": dados['name'],
            "symbol": dados['symbol'],
            "price": price
        }

        return response


api.add_resource(Bovespa, '/v1/bovespa/')
api.add_resource(SearchName, '/v1/busca/<string:nome>/')
api.add_resource(UserMethods, '/v1/user/<string:nome>/')
api.add_resource(methodPostUser, '/v1/user/')
api.add_resource(methodPostCompany, '/v1/company/')
api.add_resource(listCompanyByIdUser, '/v1/user/company/<int:id>/')
api.add_resource(companyMethods, '/v1/company/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
