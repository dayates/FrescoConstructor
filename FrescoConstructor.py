#main function

#imports
import numpy as np
import pandas as pd
import re
from dataclasses import dataclass

#user-written imports
from ame_masses import *
from calculations import *
from construction_functions import *
from constructor import *
from inputs import *
from isotope import *
from potentials import *



mass_df = get_AME_masses()

Fresco_constructor(mass_df)
