class CanonicalFormReduction:

    @staticmethod
    def _find_perfect_joint_edge(node: object, relationships: list):
        # Find Perfect & Joint edges
        perfect_edges, joint_edges = [], []
        for edge in relationships:
            for element in edge["elements"]:
                if node["name"] == element["name"]:
                    if edge["type"] == "perfect" or edge["type"] == "joint":
                        for element_reference in edge["elements"]:
                            if node["name"] == element_reference["name"]:
                                continue
                            elif edge["type"] == "perfect":
                                perfect_edges.append(element_reference["name"])
                            elif edge["type"] == "joint":
                                joint_edges.append(element_reference["name"])
                            break
                    break
        return perfect_edges, joint_edges


    @staticmethod
    def _find_joint_edge(node: object, relationships: list):
        # Find Joint edges
        joint_edges = []
        for edge in relationships:
            for element in edge["elements"]:
                if node["name"] == element["name"]:
                    if edge["type"] == "joint":
                        for element_reference in edge["elements"]:
                            if node["name"] == element_reference["name"]:
                                continue
                            else:
                                joint_edges.append(element_reference["name"])
                    break
        return joint_edges
    

    @staticmethod
    def reduce_graph(elements: list, relationships: list, debug=False):
        # PJJ Reduction
        for node in elements:
            # Establise a node with at least 1 perfect edge and at least 1 joint edge
            perfect_edges, joint_edges = CanonicalFormReduction._find_perfect_joint_edge(node, relationships)
            if len(perfect_edges) < 1 or len(joint_edges) < 1:
                continue
            if debug:
                print(f"Origin Node {node['name']} Perfect Edges: {perfect_edges} Joint Edges: {joint_edges}")
            # Find Triangle N^1[P^N^2, J^N^3] -> N^2[P^N^1, J^N^3] -> N^3[J^N^1, J^N^2]
            for perfect_edge in perfect_edges:
                # Find the Reference Joint Edges for the Perfect Edge
                referece_perfect_edge_search_joint_edges = []
                for reference_node in elements:
                    if perfect_edge == reference_node["name"]:
                        # Ensure Perfect edge node also has a PJ Relationship
                        reference_perfect_edge_perfect_edges, reference_perfect_edge_joint_edges = CanonicalFormReduction._find_perfect_joint_edge(reference_node, relationships)
                        if len(reference_perfect_edge_perfect_edges) < 1 or len(reference_perfect_edge_joint_edges) < 1:
                            break
                        # Ensure one of the Perfect edge nodes perfect edges is to the Perfect edge
                        sanity_check = False
                        for reference_perfect_edge in reference_perfect_edge_perfect_edges:
                            if node["name"] == reference_perfect_edge:
                                sanity_check = True
                                break
                        # Set the search joint edges
                        if sanity_check:
                            referece_perfect_edge_search_joint_edges = reference_perfect_edge_joint_edges
                        break
                if len(referece_perfect_edge_search_joint_edges) < 1:
                    continue
                if debug:
                    print(f"Found node {perfect_edge} which referes back to {node['name']} via a perfect edge and searching for joint edges {referece_perfect_edge_search_joint_edges}")
                # Find Joint
                for joint_edge in joint_edges:
                    for search_joint_edge in referece_perfect_edge_search_joint_edges:
                        if joint_edge != search_joint_edge:
                            continue
                        if debug:
                            print(f"Found node {joint_edge} which is in search {referece_perfect_edge_search_joint_edges} and in origin {joint_edges}, which referes back to {node['name']} and {perfect_edge} via a joint edges")
                        # Established that there is a Joint from N^1 -> N^3 and N^2 -> N^3, Could stop here, but do a sanity check that N^3 -> N^1 and N^3 -> N^3
                        for reference_node in elements:
                            if joint_edge == reference_node["name"]:
                                # Ensure Joint Edge Node only has a JJ Relationship
                                reference_joint_edge_joint_edges = CanonicalFormReduction._find_joint_edge(reference_node, relationships)
                                if len(reference_joint_edge_joint_edges) < 2:
                                    break
                                # Ensure one of the Joint edge nodes joint edges is to the Origin node and another one of the joint edges is to the Perfect edge
                                node_1_found, node_2_found = False, False
                                for reference_joint_edge in reference_joint_edge_joint_edges:
                                    if node["name"] == reference_joint_edge:
                                        node_1_found = True
                                    elif perfect_edge == reference_joint_edge:
                                        node_2_found = True
                                # Remove Relationship
                                if node_1_found and node_2_found:
                                    if debug:
                                        print(f"Checked that Node 3 ({joint_edge}) has joint edges to {node['name']} and {perfect_edge}")
                                    for edge in relationships:
                                        if edge["type"] == "joint":
                                            perfect_found, joint_found = False, False
                                            for reference_edge_node in edge["elements"]:
                                                if perfect_edge == reference_edge_node["name"]:
                                                    perfect_found = True
                                                elif joint_edge == reference_edge_node["name"]:
                                                    joint_found = True
                                            if perfect_found and joint_found:
                                                if debug:
                                                    print(f"Found Relationship to remove {edge['name']}")
                                                relationships.remove(edge)
                                                #Recursive Call
                                                return CanonicalFormReduction.reduce_graph(elements, relationships, debug=debug)
                                break
                        break
        return elements, relationships