#calculations functions

#user-written imports
from masses import ame_masses
from masses.ame_masses import *
from calculations import *
#from calculations import calculate_deuteron_binding_energy
from construction_functions import *
#from constructor import *
from inputs import *
from isotope import *
from potentials import *

#L transfer calculation
def calculate_L_transfer(beam,target,ejectile,recoil):

    parity_change = beam.parity * recoil.parity

    #calculate the two possible L transfers
    L_transfer1 = abs(recoil.spin - beam.spin - (target.spin-ejectile.spin))
    L_transfer2 = abs(recoil.spin - beam.spin + (target.spin-ejectile.spin))

    #now determine which one is needed based on the parity changes
    if (+1 == parity_change):
        if (0 == L_transfer1 % 2):
            recoil.L_transfer = L_transfer1
        else:
            recoil.L_transfer = L_transfer2
    else:
        if (0 == L_transfer1 % 2):
            recoil.L_transfer = L_transfer2
        else:
            recoil.L_transfer = L_transfer1
    

    return


#determine transferred particle function
def calculate_transferred_particle(beam,recoil,mass_df):
    A = abs(beam.A - recoil.A)
    Z = abs(beam.Z - recoil.Z)
    #check if we have a neutron:
    if (0 == Z):
        transferred_particle = Isotope(A,"n",mass_df) 
    else:
        transferred_particle = Isotope(A,atomicElements[Z-1],mass_df) #-1 because we index at 0

    return transferred_particle


#binding energy calculation
def calculate_binding_energy(recoil,bound_nucleus,mass_df):
    
    #first calculate A and Z/element for the core
    A = recoil.A - bound_nucleus.A
    Z = recoil.Z - bound_nucleus.Z
    element = atomicElements[Z-1]
    core = Isotope(A,element,mass_df)

    #binding energy calculation here
    BE = core.mass + bound_nucleus.mass - recoil.mass
    #print(BE)
    recoil.binding_energy = BE
    
    return


#binding energy of the deuteron specifically
def calculate_deuteron_binding_energy(mass_df):
    deut = Isotope(2,"H",mass_df)
    prot = Isotope(1,"H",mass_df)
    neut = Isotope(1,"n",mass_df)

    return  (prot.mass + neut.mass) - deut.mass


#functions to determine the recoil based on the ejectile
def create_recoil(beam,target,ejectile,mass_df):

    mass_number = beam.A + target.A - ejectile.A
    proton_number = beam.Z + target.Z -ejectile.Z

    element = atomicElements[proton_number-1] #-1 because we index at 0

    return Isotope(mass_number,element,mass_df)
    

#q-value calculation
def calculate_q_value(beam,target,ejectile,recoil):
    initial_mass = beam.mass + target.mass #in MeV
    final_mass = ejectile.mass + recoil.mass #MeV
    q_val = initial_mass - final_mass #q value is always the same for a given reaction no matter the excitation energy

    recoil.q_value = q_val
    return

#calculation of number of nodes
def calculate_number_nodes(isotope):

    #calculate Q
    Q = 2*(isotope.orbital_osc_shell) + isotope.orbital_L

    isotope.nn = (Q-isotope.L_transfer)/2.
    

    return

