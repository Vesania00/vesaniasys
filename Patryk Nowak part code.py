def createFunModuleGraph(path="./"):
    g = networkx.DiGraph()  # create direct graph
    files_to_parse = get_python_files(path)  # only python files
    tmp_f_t_p = files_to_parse
    print(tmp_f_t_p)
    for file in files_to_parse:
        count = 0
        this_file = file
        list_of_file_fun = get_functions_names_from_file(file)
        #
        for func in list_of_file_fun:
            for fl in files_to_parse:
                if fl == this_file:
                    g.add_node(func)
                else:
                    count = count + count_method1(path + "/" + fl, func)
        g.add_node(extract_filename(file), weight=count)
        count = 0

    for file in tmp_f_t_p:
        count = 0
        this_file = file
        list_of_file_fun = get_functions_names_from_file(file)
        print(list_of_file_fun)
        for func in list_of_file_fun:
            for fl in tmp_f_t_p:
                if fl == this_file:
                    tmp_count = count_method1(path + "/" + fl, func)
                    g.add_edge(func, extract_filename(file), weight=tmp_count)
                else:
                    count = count_method1(path + "/" + fl, func) + count_method1(path + "/" + file, func)

        g.add_edge(extract_filename(file), extract_filename(fl), weight=count)

    matplotlib.pyplot.figure()
    pos = networkx.spring_layout(g)
    networkx.draw(g, pos, with_labels=True, font_weight='bold')

    pos_attr = {}
    for node, coords in pos.items():
        pos_attr[node] = (coords[0], coords[1] + 00.07)

    node_attr = networkx.get_node_attributes(g, 'weight')
    custom_node_attrs = {}
    for node, attr in node_attr.items():
        custom_node_attrs[node] = str(attr)

    edge_labels = dict([((u, v), d['weight']) for u, v, d in g.edges(data=True)])
    networkx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)

    networkx.draw_networkx_labels(g, pos_attr, labels=custom_node_attrs)
    ##
    matplotlib.pyplot.show()