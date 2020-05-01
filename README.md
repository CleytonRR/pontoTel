
# PontoTel challenge

Desafio realizado para o processo de seleção da Pontotel.

Objetivo era criar uma API com endpoints que retornam o valor de cotação da BOVESPA e de outras empresas.

## Configurando o backend
### pré-requisitos
Git e Docker
Para instalar consulte: 
* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/)

### Configuração backend :whale:
Para uma perfeita instalação é necessário o git e o docker
```sh
$ git clone git@github.com:CleytonRR/pontoTel.git
$ cd pontoTel
$ cd app
$ docker build -t pontocotacao:latest .
$ docker run -d -p 5000:5000 pontocotacao
```
## Executando: :fire:
**Com o container docker em funcionamento**

### Frontend:
basta abrir em um navegador o arquivo index.html que está na pasta frontend

### Documentação :clipboard:
Para consultar a documentação da API:
basta acessar: http://0.0.0.0:5000/apidocs/


**Observação**:
O desafio tinha de forma opcional a implementação de rotas cruds para algumas entidades, eu fiz as rotas e o crud utilizando o banco postgres, porém tive dificuldades com o docker-compose, e não consegui implementar o banco de dados no container, **deixei as rotas de crud apenas para efeito de consulta**.

## Tecnologias utilizadas
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Framework web mínimo
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) - Uma extensão do flask que facilita a escrita de API-restFul
* [Swagger](https://swagger.io/) - Utilizado para fazer a documentação do projeto
* [sqlalchemy](https://www.sqlalchemy.org/) - Um ORM para banco de dados
* [alpha vantage wrapper](https://github.com/RomelTorres/alpha_vantage) - Biblioteca que auxilia na consulta de dados da Alpha Vantage 
* [Axios](https://github.com/axios/axios) - Usado para buscar dados do backend
* [Slick](http://kenwheeler.github.io/slick/) - Usado para fazer o slider

## Desafio
- [x] (Back) Crie um endpoint que retorne o número de pontos do bovespa no formato JSON, utilizando o alpha vantage
- [x] (Front) Apresente o número de pontos do bovespa em uma página html.
- [x] (Back) Crie um endpoint que recebe as informações de uma empresa e retorne o seu atual valor no formato JSON.
- [x] (Back) Valide o input da API para garantir que ela sempre esteja correta.
- [x] (Back) Escreva testes para api.
- [x] (Front) Escolha algumas empresas(ex: Petrobras(PETR4), Itaú Unibanco(ITUB4) e Vale(VALE3))  e em uma página html deixe o usuário selecione uma delas para realizar a consulta do seu preço no momento.
### Opcional
- [x] (DB) Modele Usuário, Empresa e Cotação em um banco de dados relacional (Postgres).
- [x] (Back) Para cada um dos modelos acima crie uma rota CRUD.
- [ ] (Front) Em uma página html, deixe o usuário adicionar uma empresa para a qual ele quer consultar o seu preço.
### Pontos extras
- [x] Documentação da API com swagger
- [x] Async
- [ ] Cache
- [ ] Tipagem
- [x] Docker


