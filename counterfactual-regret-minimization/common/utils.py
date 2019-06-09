def init_sigma(node, output = None):
    # print('node', node)
    output = dict()
    def init_sigma_recursive(node):
        # print('inf_set', node.inf_set)
        output[node.inf_set()] = {action: 1. / len(node.actions) for action in node.actions}
        # print('node_children_output', output)
        for k in node.children:
            # print('children', k)
            init_sigma_recursive(node.children[k])
    init_sigma_recursive(node)
    return output

def init_empty_node_maps(node, output = None):
    output = dict()
    def init_empty_node_maps_recursive(node):
        output[node.inf_set()] = {action: 0. for action in node.actions}
        for k in node.children:
            init_empty_node_maps_recursive(node.children[k])
    init_empty_node_maps_recursive(node)
    return output
