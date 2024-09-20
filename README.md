# Projeto Final - INF325 - Grupo 5

Esse projeto contém a implementação dos schemas e bancos de dados escolhidos para o trabalho final da disciplina INF325. Foram escolhidos dois bancos de dados para a solução, PortgreSQL e Neo4J, executados internamente a um jupyter notebook para permitir facilidade nas consultas e exibidção de dados.

### 🔧 Instalação

#### Para a aplicação funcionar, é necessário lançar um contêiner local a partir de um repositório Git remoto usando [repo2docker](https://github.com/jupyter/repo2docker)

1. No terminal, entre em uma pasta de sua preferência e crie um novo ambiente virtual Python (venv):
```bash
python3 -m venv venv
```

2. Ative o seu ambiente virtual (você pode repetir este passo mais tarde se quiser reiniciar seu contêiner):
```bash
source venv/bin/activate
```

3. Instale ou atualize as bibliotecas Python necessárias usando pip:
```bash
pip install jupyter-repo2docker pip -U
```

4. Inicie o contêiner Docker usando repo2docker diretamente do repositório remoto:

```bash
jupyter-repo2docker -p 8888:8888 https://github.com/inf300-grupo5/inf325-projeto-final \ 
                    jupyter lab --ip 0.0.0.0 --NotebookApp.token=''
```

A interface estará disponível em: http://127.0.0.1:8888/lab

## 🛠️ Construído com

* [Docker](https://www.docker.com)
* [Binder](https://mybinder.org)
* [Postgresql](https://www.postgresql.org)
* [Neo4J](https://neo4j.com/product/neo4j-graph-database/)