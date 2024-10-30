#main function

#imports
import numpy as np
import pandas as pd
import re
from dataclasses import dataclass

#user-written imports
from masses import *
from calculations import *
from construction_functions import *
from constructor import *
from inputs import *
from isotope import *
from potentials import *


#execute the code
if __name__ == '__main__':

	#get our mass dataframe
	mass_df = get_AME_masses()

	#use the mass dataframe to execute the FRESCO constructor
	Fresco_constructor(mass_df)
