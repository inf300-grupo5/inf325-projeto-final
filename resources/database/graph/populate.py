import time

import psycopg2
from py2neo import Graph, Node, Relationship, ServiceUnavailable


def connect_to_neo4j():
    while True:
        try:
            graph = Graph("bolt://127.0.0.1:7687")
            graph.run("RETURN 1")
            print("Conectado ao Neo4j!")
            return graph
        except ServiceUnavailable as e:
            print("Neo4j não está disponível, tentando novamente em 5 segundos...")
            time.sleep(5)  # Espera 5 segundos antes de tentar novamente
        except Exception as e:
            print(f"Erro inesperado: {e}")
            time.sleep(5)


def get_all_products():
    try:
        connection = psycopg2.connect(
            user="postgres",
            host="127.0.0.1",
            port="5432",
            database="ecommerce"
        )

        cursor = connection.cursor()

        query = "SELECT * FROM products;"
        cursor.execute(query)

        products = cursor.fetchall()

        for product in products:
            insert_product_into_neo4j(product)

        query = "SELECT id,username FROM USERS;"
        cursor.execute(query)
        users = cursor.fetchall()
        for user in users:
            insert_user_into_neo4j(user)

        query = "SELECT u.id AS user_id, p.id AS product_id " \
                "FROM Users u " \
                "JOIN Orders o ON u.id = o.user_id " \
                "JOIN Orders_items oi ON o.id = oi.order_id " \
                "JOIN Products p ON oi.product_id = p.id " \
                "ORDER BY u.id;"

        cursor.execute(query)
        purchases = cursor.fetchall()

        for purchase in purchases:
            create_relation_in_log4j(purchase)

    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar ao PostgreSQL", error)


def create_relation_in_log4j(purchase):
    user_id = purchase[0]
    product_id = purchase[1]
    user_node = graph.nodes.match("User", system_id=user_id).first()
    product_node = graph.nodes.match("Product", system_id=product_id).first()

    if user_node and product_node:
        relationship = Relationship(user_node, "PURCHASED", product_node)
        graph.create(relationship)
        print(f"Relação criada: {user_node['username']} comprou {product_node['title']}")
    else:
        print(f"Erro: Usuário ou Produto não encontrado para user_id={user_id}, product_id={product_id}")


def insert_user_into_neo4j(user):
    system_id = user[0]
    username = user[1]
    n = Node("User", username=username,
             system_id=system_id)
    print(f"Criando Node do tipo User com o nome {username}")
    graph.create(n)


def insert_product_into_neo4j(product):
    system_id = product[0]
    title = product[1]
    parental_guidance = product[3]
    genre = product[7]
    system = product[9]

    # print(title, parental_guidance, genre, system)
    n = Node("Product", title=title,
             parental_guidance=parental_guidance,
             genre=genre,
             system=system,
             system_id=system_id)
    print(f"Criando Node do tipo Product com o nome {title}")
    graph.create(n)


if __name__ == '__main__':
    graph = connect_to_neo4j()
    get_all_products()
