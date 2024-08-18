from yfiles_jupyter_graphs_for_neo4j import Neo4jGraphWidget
from neo4j import GraphDatabase
from yfiles_jupyter_graphs import GraphWidget
from IPython.core.magic import (register_line_magic,
                                register_cell_magic)

driver = GraphDatabase.driver(uri = "neo4j://localhost")

def query_neo4j(cypher_query: str):
    query_graph_result = driver.session().run(cypher_query).graph()
    graph_widget = GraphWidget(overview_enabled=False, context_start_with='Data', graph = query_graph_result)
    graph_widget.set_sidebar(enabled=False, start_with='Data')
    display(graph_widget)
    return graph_widget

def cypher(line, cell_content):
    print(line)
    query_neo4j(cell_content)

def load_ipython_extension(ipython):
    """This function is called when the extension is
    loaded. It accepts an IPython InteractiveShell
    instance. We can register the magic with the
    `register_magic_function` method of the shell
    instance."""
    ipython.register_magic_function(cypher, 'cell')
    
