from graphviz import Digraph

def create_tree_image(data, file):
    graph = Digraph()
    def traverse(node, parent_id=None):
        node_id = str(id(node))
        graph.node(node_id, label=node["type"])
        if parent_id:
            graph.edge(parent_id, node_id)
        for child in node.get("children", []):
            traverse(child, node_id)
    traverse(data)
    graph.render(file, format="png", view=False)
