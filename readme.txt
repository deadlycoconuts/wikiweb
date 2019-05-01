1. Open my_spider.py. Enter and verify that: 

	HOME_URL = [your desired start URL as a string] (line 11)
	MAX_LEVEL = [your desired branching level; 0 for solely the home page, 1 for the pages that stem from the home page..] (line 12)
   
	Save my_spider.py

2. Run the command:
	scrapy runspider my_spider.py -o [name of json file]

	!!! IMPORTANT: Ensure that the json file DOES NOT already exist within the directory, failing which the spider will continue writing on the pre-existing file.

3. Choose to proceed with either step 3a or step 3b.

	3a. To create a png image with graph_tool on python:
		i) Run the command:
			python3 my_graph_builder.py [name of json file]
		
		   A png file containing the graph titled "graph" will appear within the directory.

	3b. To project the graph as an interactive display on your browser:
		i) Run the command:
			python3 my_cleanup.py [name of json file]
			
		   2 json files titled "nodeList" and "linkList" should appear within the directory.

		ii) Open the HTML document titled "wikiweb".
			
		    You should be able to:
			- click and drag on any node to manipulate the entire graph
			- click on any node to show only its immediate neighbours
			- click again on the same node previously clicked on to display the entire graph