#functions for constructing the output file

#user-written imports
from masses import *
from constructors.calculations import *
#from calculations import calculate_deuteron_binding_energy
from constructors.construction_functions import *
#from constructor import *
from constructors.inputs import *
from constructors.isotope import *
from constructors.potentials import *

#initial setup of the FRESCO header info. This is mostly unchanged from reaction to reaction
def construct_fresco_header(lab_energy):

    file = open('build_template_files/NAMELIST.txt','r')
    namelist_header = file.read()
    namelist_header = namelist_header.replace("LAB_ENERGY",str(lab_energy)) #lab energy in MeV
        
    #print(namelist_header)

    return namelist_header


#partition function
def construct_partition(beam,target,recoil,num_states): #beam is a tuple of A,El,mass
    file = open('build_template_files/PARTITION.txt','r')
    partition_info = file.read()

    #unpack tuples
    #A,El,mass = beam
    #A_targ, El_targ, mass_targ = target

    #reassign parts
    partition_info = partition_info.replace('BEAM_ISOTOPE',"' "+beam.isotope+"'")
    #print(type(mass))
    partition_info = partition_info.replace('BEAM_MASS',str(round(float(beam.mass_amu),3)))
    partition_info = partition_info.replace('BEAM_Z', str(beam.Z)) #plus one because we index at 0, but periodic table indexes as t
    partition_info = partition_info.replace('TARGET_NAME',"' "+target.isotope+"'")
    partition_info = partition_info.replace('TARGET_MASS',str(round(float(target.mass_amu),3)))
    partition_info = partition_info.replace('TARGET_Z',str(target.Z)) #plus one because of indexing again
    partition_info = partition_info.replace('Q_VALUE',str(round(recoil.q_value,3)))
    partition_info = partition_info.replace('NUM_STATES',str(num_states))
    
    #print(partition_info)
    return partition_info


#state function
def construct_states(beam,target,recoil):
    file = open('build_template_files/STATE.txt','r')
    state_info = file.read()


    state_info = state_info.replace('BEAM_J',str(beam.spin))
    state_info = state_info.replace('BEAM_PARITY',str(beam.parity))
    state_info = state_info.replace('BEAM_EXC_ENERGY',str(beam.exc_energy))
    state_info = state_info.replace('TARGET_J',str(target.spin))
    state_info = state_info.replace('TARGET_PARITY',str(target.parity))
    state_info = state_info.replace('Q_VALUE',str(round(recoil.q_value,3)))
    
    #print(state_info)
    return state_info


#overlap function
def construct_overlap(recoil,number):
    file = open('build_template_files/OVERLAP.txt')
    overlap_info = file.read()

    overlap_info = overlap_info.replace('STATE_NUM',number)
    overlap_info = overlap_info.replace('STATE_NN',str(recoil.nn))
    overlap_info = overlap_info.replace('STATE_L',str(recoil.orbital_L))
    overlap_info = overlap_info.replace('STATE_J',str(recoil.orbital_J))
    overlap_info = overlap_info.replace('STATE_SN',str(round(recoil.binding_energy - recoil.exc_energy,3)))

    #this is needed to change the potential used for the deuteron only
    if ("2H" == recoil.isotope):
        overlap_info = overlap_info.replace('ic1=2','ic1=1')
        overlap_info = overlap_info.replace('ic2=1','ic2=2')
        overlap_info = overlap_info.replace('in=1','in=2')
        overlap_info = overlap_info.replace('kbpot=5','kbpot=4')

    return overlap_info


#coupling header
def construct_coupling():
    file = open('build_template_files/COUPLING.txt')
    coupling_info = file.read()

    return coupling_info


#cfp info
def construct_cfp(state_num):
    file = open('build_template_files/CFP.txt')
    cfp_info = file.read()

    #if we have a deuteron, do something extra:
    if ("" == state_num):
        cfp_info = cfp_info.replace("in=1","in=2")
    
    cfp_info = cfp_info.replace('STATE_NUM',state_num)

    return cfp_info


#this will construct the potential 
def construct_potential(isotope,potential,beam_energy,number):
    file = open('build_template_files/POTENTIAL.txt')
    potential_info = file.read()
    
    #replace the stuff we need now
    potential_info = potential_info.replace('MASS',str(isotope.A))
    potential_info = potential_info.replace('RC',str(potential.RC))
    potential_info = potential_info.replace('KP_NUM',str(number))
    potential_info = potential_info.replace('V0',str(round(potential.V0,4)))
    potential_info = potential_info.replace('R0',str(round(potential.R0,4)))
    potential_info = potential_info.replace('A0',str(round(potential.A0,4)))
    if (3 != number):#only do these if we aren't in the beam+neutron potential
        potential_info = potential_info.replace('WD',str(round(potential.WD,4)))
        potential_info = potential_info.replace('RD',str(round(potential.RD,4)))
        potential_info = potential_info.replace('AD',str(round(potential.AD,4)))
        potential_info = potential_info.replace('VL',str(round(potential.VLS,4)))
        potential_info = potential_info.replace('RL',str(round(potential.RLS,4)))
        potential_info = potential_info.replace('AL',str(round(potential.ALS,4)))

    return potential_info


#this constructs the deuteron binding potential. Not dependent on the beam
def construct_deuteron_potential():
    file = open('build_template_files/DEUTERON_POTENTIAL.txt')
    deut_info = file.read()

    return deut_info
