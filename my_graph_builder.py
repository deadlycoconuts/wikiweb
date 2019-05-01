# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 16:27:30 2019

@author: Ewe
"""

from graph_tool.all import *
import json
import sys

def clean_up_data(fileName):
    f = open(fileName, 'r+')
    data = f.read()
    if data[-1] != "]": # invalid JSON file
        if data[-1] == "}": # last dictionary entry is complete
            data += "]"
        else: # incomplete dictionary entry
            f.seek(0)
            lines = f.readlines()
            with open(fileName, 'w') as f: # rewrites json file with incomplete line removed
                f.write(''.join(lines[:-1]))
            
            f = open(fileName, 'r') # reopens file
            data = f.read() # reads file as string of characters
            data = data[:-2] + "]" # removes newline and comma characters
    
        f.close()
        #print("ALMOST DONE")
        with open(fileName, 'w') as f:
            f.write(''.join(data))
    return

def get_data(fileName):
    clean_up_data(fileName)
    with open(fileName) as f:
        dataset = json.load(f)    
    return dataset

def proc_data(dataset): 
    # creates a list to store all urls found
    urls = list(set([ data['self_url'] for data in dataset ])) # removes URL duplicates from self_urls
    urls.extend(list(set([ data['ext_url'] for data in dataset ]))) # adds other URLs branches to list
    url_to_idx = { url:i for i, url in enumerate(urls) }
    #print(len(urls) - len(url_to_idx)) # solve this
    mod_dataset = []
    node_to_title = {}
    for data in dataset:
        mod_dataset.append((url_to_idx[data['self_url']],url_to_idx[data['ext_url']],data['self_title'],data['ext_title']))
        # creates dictionary which maps node number to page title
        node_to_title[url_to_idx[data['self_url']]] = data['self_title']
        node_to_title[url_to_idx[data['ext_url']]] = data['ext_title']
    # return modified dataset
    return mod_dataset, len(urls), node_to_title

def build_graph(dataset,node_count, node_to_title):
    g = Graph()
    g.add_vertex(node_count)
    # label -> title
    label = g.new_edge_property('string')
    
    # labels all vertices with their page titles
    vertices_labels = g.new_vertex_property('string')
    for key, item in node_to_title.items():
        vertices_labels[key] = item
        
    for n1,n2,t1,t2 in dataset:
        # connect nodes
        e = g.add_edge(n1,n2)
        # name edge
        label[e] = t2
    # return the graph
    return g, label, vertices_labels


if __name__ == '__main__':
    dataset, node_count, node_to_title = proc_data(get_data(sys.argv[1]))
    g, label, vertices_labels = build_graph(dataset, node_count, node_to_title)
    graph_draw(g, vertex_text=vertices_labels, vertex_font_size=13, edge_text_distance=30, edge_marker_size=10,output_size=(7500, 7500), output="graph.png")