#main function

#imports
import numpy as np
import pandas as pd
import re
from dataclasses import dataclass

#user-written imports
from masses import *
from constructors.calculations import *
from constructors.construction_functions import *
from constructors.constructor import *
from constructors.inputs import *
from constructors.isotope import *
from constructors.potentials import *
#from constructors import *

#execute the code
if __name__ == '__main__':

	#get our mass dataframe
	mass_df = get_AME_masses()

	#use the mass dataframe to execute the FRESCO constructor
	Fresco_constructor(mass_df)
