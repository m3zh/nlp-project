from datetime import datetime
from datetime import date
import os
import zipfile
import pandas_utils
import search_db.pubmed as search_db_pubmed
import search_db.crossref as search_db_crossref
import search_db.pyscopus as search_db_scopus
import search_db.google_scholar.search_utilities as search_db_gs
import search_db.frontiersin as search_db_frontiersin

# words to research without operators
search_no_operators = "gifted+attachment"
# words to research with operators
search_with_operators = "gifted attachment" #OPERATORS doesnt work with pubmed
# name of client
name_client = input('Please enter name of client : ')
id_results = str("{0}_{1}_{2}".format(search_no_operators, name_client, date.today()))
## create client's folder
os.mkdir("./excels/{0}".format(id_results))
## create file to store effectvive count (PRISMA method)
prisma_file = open("./excels/{0}/records_numbers.txt".format(id_results),"w+")



# DataFrame FEEDERS
## Feed it with PUBMED
df_pubmed = search_db_pubmed.pubmed_df_feeder(search_with_operators)
print("✓ Pubmed, n=", len(df_pubmed))
## Feed it with CROSSREF
df_crossref = search_db_crossref.crossref_df_feeder(search_no_operators)
print("✓ Crossref, n=", len(df_crossref))
## Feed it with ELSEVIER
df_elsevier = search_db_scopus.scopus_df_feeder(search_no_operators)
print("✓ Scopus, n=", len(df_elsevier))
## Feed it with GOOGLE SCHOLAR
df_gs = search_db_gs.gs_df_feeder(search_no_operators)
print("✓ Google Scholar, n=", len(df_gs))
## Feed it with FRONTIERSIN
df_frontiersin = search_db_frontiersin.frontiersin_df_feeder(search_no_operators)
print("✓ Frontiersin, n=", len(df_frontiersin))

# Merge DataFrame filled by databases
df_full = pandas_utils.df_full_merging(df_crossref, df_pubmed, df_elsevier, df_gs, df_frontiersin)
## Print lenght of index (number of rows)
print("Number of results before cleaning :", len(df_full))
prisma_file.write("Records identified trough databases searching :" + str(len(df_full)) + "\n")

# Cleaning the whole set
# df_clean= df_full.drop_duplicates(subset=['DOI'], keep='last')
# df_clean.reset_index(drop=True, inplace=True)
prisma_file.write("Records identified after duplicates removal :" + str(len(df_full)) + "\n") # no cleaning

# Export merged DataFrame to files
df_full.to_csv("./excels/{0}/results.csv".format(id_results))
print("Results exported to .csv in ./excels/{0}/".format(id_results))
## Close PRISMA file
prisma_file.close()

# Sorting model
## took a df.csv and return df.xlsx 


# Create and export to zip
final_zip = zipfile.ZipFile("./excels/{0}/{0}.zip".format(id_results), "w", zipfile.ZIP_DEFLATED)
final_zip.write("./excels/{0}/results.csv".format(id_results))
final_zip.write("./excels/{0}/records_numbers.txt".format(id_results))
final_zip.close()
