import pandas as pd
from yfiles_jupyter_graphs_for_neo4j import Neo4jGraphWidget
from neo4j import GraphDatabase
from yfiles_jupyter_graphs import GraphWidget
from IPython.core.magic import (register_line_magic,
                                register_cell_magic)
from IPython.display import IFrame
import json
import uuid
import os
from py2neo import Graph


driver = GraphDatabase.driver(uri = "neo4j://localhost")


def vis_network(nodes, edges, physics=True):
    html = """
    <html>
    <head>
      <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
      <meta content="utf-8" http-equiv="encoding">    
      <script type="text/javascript" src="https://thedatasociety.github.io/resources/purl/lab-neo4j/graphdrawer/vis.js"></script>
      <link   type="text/css"       href="https://thedatasociety.github.io/resources/purl/lab-neo4j/graphdrawer/vis.css" rel="stylesheet" >
    </head>
    <body>

    <div id="{id}"></div>

    <script type="text/javascript">
      var nodes = {nodes};
      var edges = {edges};

      var container = document.getElementById("{id}");

      var data = {{
        nodes: nodes,
        edges: edges
      }};

      var options = {{
          nodes: {{
              shape: 'dot',
              size: 25,
              font: {{
                  size: 14
              }}
          }},
          edges: {{
              font: {{
                  size: 14,
                  align: 'middle'
              }},
              color: 'gray',
              arrows: {{
                  to: {{enabled: true, scaleFactor: 0.5}}
              }},
              smooth: {{enabled: false}}
          }},
          physics: {{
              enabled: {physics}
          }}
      }};

      var network = new vis.Network(container, data, options);

    </script>
    </body>
    </html>
    """

    unique_id = str(uuid.uuid4())
    html = html.format(id=unique_id, nodes=json.dumps(nodes), edges=json.dumps(edges), physics=json.dumps(physics))

    try:
        os.makedirs('graphs')
    except OSError as e:
        pass 
    
    filename = "resources/graphs/graph-{}.html".format(unique_id)

    file = open(filename, "w+")
    file.write(html)
    file.close()

    return IFrame(filename, width="100%", height="450")

def draw(graph, options, physics=False, limit=300):
    # The options argument should be a dictionary of node labels and property keys; it determines which property
    # is displayed for the node label. For example, in the movie graph, options = {"Movie": "title", "Person": "name"}.
    # Omitting a node label from the options dict will leave the node unlabeled in the visualization.
    # Setting physics = True makes the nodes bounce around when you touch them!
    query = """
    MATCH (n)
    WITH n, rand() AS random
    ORDER BY random
    LIMIT 300
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n AS source_node,
           id(n) AS source_id,
           r,
           m AS target_node,
           id(m) AS target_id
    """

    data = graph.run(query, limit=limit)

    nodes = []
    edges = []

    def get_vis_info(node, id):
        node_label = list(node.labels)[0]
        prop_key = options.get(node_label)
        vis_label = node['label']
        
        if node['label'] == None:

            return {
                    "id": id, 
                    "label": "\n{}".format(node.labels), 
                    "group": node_label, "title": "Type(s) = {} <br/> Properties = ".format(node_label)+repr(dict(node))
                   }
        else:

            return {
                    "id": id, 
                    "label": "\n\n{} ({})".format(node.labels,node['label']), 
                    "group": node_label, "title": "Type(s) = {} <br/> Properties = ".format(node_label)+repr(dict(node))
                   }

    
    for row in data:
        source_node = row[0]
        source_id = row[1]
        rel = row[2]
        target_node = row[3]
        target_id = row[4]

        source_info = get_vis_info(source_node, source_id)

        if source_info not in nodes:
            nodes.append(source_info)

        if rel is not None:
            target_info = get_vis_info(target_node, target_id)

            if target_info not in nodes:
                nodes.append(target_info)

            edges.append({"from": source_info["id"], "to": target_info["id"], "label": "{}".format(type(rel).__name__)})

    return vis_network(nodes, edges, physics=physics)

def print_counters(counters):
    for attr in dir(counters):
        # Filter out private methods and attributes
        if not attr.startswith('_'):
            value = getattr(counters, attr)
            if isinstance(value, int):
                if value > 0:
                    print(f"{attr.replace('_', ' ').capitalize()}: {value}")

def query_neo4j_output_graph(cypher_query: str):
    query_graph_result = driver.session().run(cypher_query)
    graph_widget = GraphWidget(overview_enabled=False, context_start_with='Data', graph = query_graph_result.graph())
    graph_widget.set_sidebar(enabled=False, start_with='Data')
    print_counters(query_graph_result.consume().counters)
    display(graph_widget)
    return graph_widget

def query_neo4j_output_table(cypher_query: str):
    query_graph_result = driver.session().run(cypher_query)
    df = pd.DataFrame(query_graph_result.data())
    pd.set_option('display.max_colwidth', None)
    print_counters(query_graph_result.consume().counters)
    display(df)
    return df


def query_neo4j_output_only_counter(cypher_query: str):
    query_graph_result = driver.session().run(cypher_query)
    print_counters(query_graph_result.consume().counters)
    





def cypher(line, cell_content):
    
    if line == 'show returned graph':
        query_neo4j_output_graph(cell_content)
    elif line == 'show full graph':
        if cell_content.replace(" ", "").lower().strip() != 'display':
            query_neo4j_output_only_counter(cell_content)
        graph = Graph("bolt://127.0.0.1:7687")
        iframe = draw(graph, {}, physics=True)
        display(iframe)

    else:
        query_neo4j_output_table(cell_content)

def load_ipython_extension(ipython):
    """This function is called when the extension is
    loaded. It accepts an IPython InteractiveShell
    instance. We can register the magic with the
    `register_magic_function` method of the shell
    instance."""
    ipython.register_magic_function(cypher, 'cell')
    