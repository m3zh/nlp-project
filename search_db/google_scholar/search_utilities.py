import requests
import clean_utilities as clean
import update_utilities as update
# import proxy
from bs4 import BeautifulSoup as bs
import pandas as pd
# from torrequest import TorRequest
import time
import random
import sys # needed for import pandas_utils from parent folder
sys.path.append("/...") # needed for import pandas_utils from parent folder
import pandas_utils

def selenium_search(keywords, browser, limit):
	payload = (keywords).replace(' ', '+') # change parameters keyword in url form
	df = [] # creates an empty dataframe
	for i in range(0, limit, 10):
		browser.get('https://scholar.google.com/scholar?start={0}&hl=en&as_sdt=0,5&q={1}'.format(i, payload)) #, proxies={"http": p, "https": p})
		html = browser.page_source
		# print(html)
		# print("Scraping page {} ...".format(i // 10))
		page = bs(html, "html.parser")
		data = clean.data(page)
		# print(data)
		tmp = pd.DataFrame(data, columns=['title', 'publication date', 'journal', 'DOI', 'author', 'abstract'])
		df.append(tmp)
		time.sleep(1)
	return (df)

def create_gs_df(data):
	df = pandas_utils.df_empty_creator()
	# print("ok")
	for d in data:
		# print("d in data")
		df = pd.concat([df, d], ignore_index=True)
	# df.insert(loc=2, column='subject', value="") # no subjects retrieved from google scholar yet
	df['DOI'] = df['DOI'].apply(lambda x: clean.single_DOI(x))
	# df['from_database'] = 'gs'
	# print(df)
	return (df)
