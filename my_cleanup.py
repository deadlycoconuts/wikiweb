# -*- coding: utf-8 -*-
"""
Created on Wed May  1 18:56:36 2019

@author: Ewe
"""

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
   
    nodeList = [] # to store nodes
    for url in urls:
        for data in dataset:
            if url == data["self_url"]:
                nodeList.append({"id": url, "label": data["self_title"], "level": data["current_level"]})
                break
            elif url == data["ext_url"]:
                nodeList.append({"id": url, "label": data["ext_title"], "level": data["current_level"]+1})
                break
    
    linkList = [] # to store links
    for data in dataset:
        linkList.append({"target": data["self_url"], "source": data["ext_url"], "strength": 0.7})

    with open('nodeList.json', 'w', encoding='utf-8') as json_file:
        json_file.write('[\n')
        for node in nodeList:
            json.dump(node, json_file)
            if node == nodeList[-1]:
                json_file.write("\n]")
            else:
                json_file.write(",\n")
    
    with open('linkList.json', 'w', encoding='utf-8') as json_file:
        json_file.write('[\n')
        for link in linkList:
            json.dump(link, json_file)
            if link == linkList[-1]:
                json_file.write("\n]")
            else:
                json_file.write(",\n")


if __name__ == '__main__':
    proc_data(get_data(sys.argv[1]))