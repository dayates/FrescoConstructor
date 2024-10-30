#importing the AME2020 masses
#https://www-nds.iaea.org/amdc/
#W.J. Huang et al 2021 Chinese Phys. C 45 030002
#Meng Wang et al 2021 Chinese Phys. C 45 030003

import pandas as pd

#this will unpack the AME and return a pandas DataFrame of masses
def get_AME_masses():
	#import NNDC Masses as a Pandas DataFrame
	masses = pd.read_fwf("masses/mass_1.mas20.txt",skiprows=33,infer_nrows=3500) 
	#infer rows to almost the entire thing so that it parses the larger N,Z,A values correctly

	#drop some columns we don't care about
	masses.drop(['1N-Z','O','MASS EXCESS           BINDING ENERGY/A        BETA-DECAY ENERGY'],axis=1,inplace=True)
	#drop the units underneath the header keys
	masses.drop([0],axis=0,inplace=True)

	#convert the split mass (in micro-amu) into a single micro-amu column
	masses['Atomic Mass (micro-amu)'] = masses['ATOMIC MASS'].apply(lambda x: float(x.split("#")[0])) + masses['Unnamed: 7']*1e6
	#the split("#") is needed to remove any of the "#" that appear due to estimated errors 
	#create masses in MeV
	masses['Atomic Mass (MeV)'] = masses['Atomic Mass (micro-amu)'] *931.5/1.e6 #931.5 MeV = 1 amu. Also convert from micro-amu to amu
	
	return masses