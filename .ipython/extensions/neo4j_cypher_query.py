import pandas as pd
from yfiles_jupyter_graphs_for_neo4j import Neo4jGraphWidget
from neo4j import GraphDatabase
from yfiles_jupyter_graphs import GraphWidget
from IPython.core.magic import (register_line_magic,
                                register_cell_magic)



driver = GraphDatabase.driver(uri = "neo4j://localhost")

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



def cypher(line, cell_content):
    
    if line == 'graph':
        query_neo4j_output_graph(cell_content)
    else:
        query_neo4j_output_table(cell_content)

def load_ipython_extension(ipython):
    """This function is called when the extension is
    loaded. It accepts an IPython InteractiveShell
    instance. We can register the magic with the
    `register_magic_function` method of the shell
    instance."""
    ipython.register_magic_function(cypher, 'cell')
    