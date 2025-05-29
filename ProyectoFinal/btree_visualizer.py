from graphviz import Digraph

def visualize_btree(btree):
    dot = Digraph(format='png')
    node_id = [0]

    def add_node(node):
        current_id = str(node_id[0])
        label_parts = []
        for i in range(node.n):
            label_parts.append(f"<f{i}> {node.keys[i]}")
        label = " | ".join(label_parts)
        dot.node(current_id, f'{{{label}}}', shape='record')
        node_id[0] += 1

        if not node.leaf:
            for i in range(node.n + 1):
                child = node.children[i]
                child_id = str(node_id[0])
                add_node(child)
                dot.edge(current_id + f":f{i}", child_id)

    add_node(btree.root)
    return dot
