#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pySudoc import *
"""

This example contains commented code : these part would save your request results in a json file for further usages


"""

#	We set up params for get research
#	This will search for every Thesis with Augustin in the title and Latin in the subject
#	We copy the params from the Sudoc website (after the first "?")
params = "ACT=SRCHM&MATCFILTER=Y&MATCSET=Y&NOSCAN=Y&PARSE_MNEMONICS=N&PARSE_OPWORDS=N&PARSE_OLDSETS=N&IMPLAND=Y&ACT0=SRCHA&screen_mode=Recherche&IKT0=4&TRM0=Augustin&ACT1=*&IKT1=21&TRM1=Latin&ACT2=*&IKT2=4&TRM2=&ACT3=*&IKT3=1016&TRM3=&SRT=YOP&ADI_TAA=&ADI_LND=&ADI_JVU=&ADI_MAT=Y&ILN_DEP_BIB=DEP&NOT_USED_ADI_BIB=+"

#	We get a list of singleUnits
RDFs = getSingleUnits("augustin", params, "./data/augustin/", "./data/augustin-rdf/", True)
"""
	This would write the data :
RDFs = saveData(RDFs, "./data/augustin/_index.json", "wt")
	And this would read them :
RDFs = saveData(path = "./data/augustin/_index.json")

"""
#	We look for details on rdf files
details = getDetails(RDFs, True)
"""
	This would write the data :
saveData(details, "./data/augustin/_details.json", "wt")

	And this would read them :
details = saveData(path = "./data/augustin/_details.json")
"""
#	And this would save our data in a readable spreadsheet format (CSV)
CSV(details, "./data/augustin/_results.csv")
