import requests
import random
import proxy
import search_utilities as search
import clean_utilities as clean
import update_utilities as update
from bs4 import BeautifulSoup as bs
import sys
import pandas as pd

proxies = proxy.get_started()
connection = proxy.get_session(proxies)
proxy.check_connection(connection)

#enter your search keywords, leaving a space between them, ex.: keyword1 keyword2
df = search.keywords('flower africa', limit=100) #limit -> how many results you want
#doi = update.empty_DOI(doi)
print(df)
