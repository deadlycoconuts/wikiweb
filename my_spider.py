# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 23:03:14 2019

@author: Ewe
"""

import scrapy
from bs4 import BeautifulSoup

HOME_URL = 'https://en.wikipedia.org'
MAX_LEVEL = 1 # max crawl depth

class WikipediaSpider(scrapy.Spider):
    name = 'wiki'
    currentLevel = 0
    
    def start_requests(self):
        start_urls = ['https://en.wikipedia.org/wiki/Unus_pro_omnibus,_omnes_pro_uno']
        for url in start_urls:
            yield scrapy.Request(url = url, callback = self.parse)
    
    def parse(self, response):
        print(response)
        if 'level' not in response.meta:
            currentLevel = 0
        else:
            currentLevel = response.meta['level']
        self_title = response.xpath('//h1[contains(@class,"firstHeading")]//text()').get() #uses XPath expression to search for object from HTML code, gets first matched element
        self_url = response.url # gets URL of current page to be scraped
        soup = BeautifulSoup(response.body,'lxml') # parses the HTML code of the page into the BeautifulSoup constructor using the lxml HTML parser
        
        # stores all hyperlinks found on page
        listTags = [] # list to store all hyperlinks found
        for paragraph in soup.findAll('p'): # for each paragraph found
            listTags.extend(paragraph.findAll('a')) # stores all hyperlinks found 
        
        # cleans up list of hyperlinks; retains only relevant links
        listLinks = [] # stores the name and url of each hyperlink found
        listOfFilterKeywords = ['cite_note', 'File'] # stores list of keywords that indicates links to be filtered out
        for tag in listTags:
            for keyword in listOfFilterKeywords:
                if keyword in str(tag): # checks if keyword is found; if so, skip this tag
                    continue
                if 'title' in tag.attrs and 'href' in tag.attrs: # checks if title and link elements exist in the tag
                    listLinks.append((tag['title'], HOME_URL + tag['href'])) # appends a title-url pair to listLinks
                    break
        
        for link in listLinks: # for each hyperlink found
            """
            if currentLevel == 0: # base level
                self_title = 
                """
            yield {"self_title": self_title, "self_url": self_url, "ext_title": link[0], "ext_url": link[1], "current_level": currentLevel} # stores a dictionary of the information regarding each hyperlink i.e. which page it is found on
            
            if currentLevel + 1 > MAX_LEVEL: # stops sending requests if spider is going to reach max crawl levvel
                continue
            
            request = scrapy.Request(link[1], callback=self.parse)
            request.meta['level'] = currentLevel + 1
            yield request
            #yield response.follow(link[1], callback=self.parse) # creates a new Request object using the url of each hyperlink