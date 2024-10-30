#user inputs and associated functions

#atomic element abbreviation
atomicElements = "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce P Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og".split(" ")

import numpy as np
import re

#user-written imports
from ame_masses import *
from calculations import *
#from calculations import calculate_deuteron_binding_energy
from construction_functions import *
#from constructor import *
from inputs import *
from isotope import *
from potentials import *


#function for getting user input for 
def get_user_isotope(mass_df):

    my_iso = None
    while True:
        element = "BAD"
        mass_number = -1
        
        #get the element
        while element not in atomicElements:
            element = input("Please enter the name (ex: Kr):" )
        
        #get the mass number
        while mass_number not in range(1,300):
            try:
                mass_number = int(input("Please enter the mass number: "))
            except:
                print("Looks like you did not enter an integer!")
                
            else:
                if (mass_number not in range(1,300)):
                    print("Mass number out of range!\nMust have mass 1-300")
                    
        #create our isotope    
        my_iso = Isotope(mass_number,element,mass_df)
        if (0 == my_iso.mass):
            print(f"Isotope {my_iso.isotope} does not exist in the AME2020. Try again!")
        else:
            break
    
        #print(f'Selected isotope: {mass_number}{element}, mass {round(isotope_mass,3)} MeV')

    #now return this A,El, mass as a tuple
    #return (mass_number,element,isotope_mass)
    return my_iso


#function for the number of states
def get_user_number_states():
    num_states = -1
    while num_states < 1:
        try:
            num_states = int(input("Enter the number of states to populate: "))
        except:
            print("Number of states must be a natural number!")
        else:
            if (num_states > 0):
                return num_states


#get the energy itself
def get_user_excited_state_energy(isotope):

    energy  = -1
    while energy < 0:
        try:
            energy = float(input("Enter the excited-state energy (MeV): "))
        except:
            print("Energy must be a non-negative number!")
        else:
            if (energy >= 0):
                isotope.exc_energy = energy

    return
    



#function for populating states in the recoiling nucleus
def get_user_excited_state(isotope):

    get_user_excited_state_energy(isotope)
    get_user_spin(isotope)
    get_user_parity(isotope)

    return


#function for getting the L value of an orbital
def get_orbital_L(orbital):
    orbital_indexes = possible_orbitals = "s p d f g h i j k l".split(" ")
    try:
        L_value = orbital_indexes.index(orbital)
    except:
        return -1
    else:
        return L_value


#function for getting the associated orbital for the transfer
def get_user_orbital(isotope):
    orbital_string = "BAD"
    orbital = "BAD"

    possible_orbitals = "s p d f g h i j k l".split(" ")
    while orbital not in possible_orbitals:
        orbital_string = input("Enter the orbital (ex: 2d5/2): ")
        #split the orbital string and find just the orbital and oscillator
        try:
            shell, orbital, J = re.split(r'([a-z])',orbital_string)

        except:
            print("Not a valid orbital.")
        else:
            if orbital not in possible_orbitals:
                print("Not a valid orbital.")
            else:
                isotope.orbital_osc_shell = int(shell)
                isotope.orbital_orbital = orbital
                
                isotope.orbital_L = get_orbital_L(orbital)
                num, denom = J.split('/')
                isotope.orbital_J = float(num)/float(denom)
            #    print(shell)
            #    print(orbital)
            #    print(L)
    return



#get the spin-parity for the parent state
def get_user_spin_parity(my_isotope):

    #A,El,mass = beam
   # Z = get_proton_number(El) #find the z of our nucleus

    #if we have an even-even nucleus, return 0+
    #return the form (spin,parity) where parity is defined by +-1
    if (0 == my_isotope.A % 2) and (0 == my_isotope.Z % 2):
        print("Even-even nucleus. Using spin 0+")
        my_isotope.spin = 0
        my_isotope.parity = +1
        return

    #if we have a deuteron, we know what that is too:
    elif (2 == my_isotope.A) and ('H' == my_isotope.element):
        my_isotope.spin = 1
        my_isotope.parity = +1
        return 

    
    else:
        #get a spin that is an whole number of positive half-integer
        get_user_spin(my_isotope)

        
        #now get the parity:
        get_user_parity(my_isotope)

    return


#get spin function
def get_user_spin(isotope):
    #get a spin that is an whole number of positive half-integer
    possible_spins = np.linspace(0,20,41) #unlikely to have a spin higher than 20
    spin = -1
    
    while spin not in possible_spins:
        try:
            spin = float(input("Enter the spin: "))
        except:
            print("Spin was not a number!")
            #continue
        else:
            if (spin not in possible_spins):
                print("Spin is not an non-negative integer or half-integer!")
            else:
                isotope.spin = spin
    return


#get parity function
def get_user_parity(isotope):
    #get the parity:
    parity = 0
    while parity not in (-1,1):
        try:
            parity = int(input(u"Please enter the parity (\u00B11): "))
        except:
            print("Parity is not a number!")
        else:
            if parity not in (-1,1):
                print(u"Parity not in \u00B11")
            else:
                isotope.parity = parity
    return


#get the beam energy
def get_user_beam_energy():

    beam_energy = -1
    
    #get the beam energy
    while beam_energy < 0:
        
        try:
            beam_energy = float(input("Enter total beam energy (MeV): "))
        except:
            print("Beam energy is not a number (>0). Try again")
            #continue
        else:
            if (beam_energy > 0):
                return beam_energy



