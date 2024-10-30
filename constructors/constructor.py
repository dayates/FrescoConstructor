#construction of the file in the function here

#user-written imports
from masses import *
from constructors.calculations import *
#from calculations import calculate_deuteron_binding_energy
from constructors.construction_functions import *
#from constructor import *
from constructors.inputs import *
from constructors.isotope import *
from constructors.potentials import *

def Fresco_constructor(mass_df):

    #First, get the beam that we want for the (d,p) reaction:    
    beam_isotope = get_user_isotope(mass_df) 
    
    #get our initial spin-parity values
    get_user_spin_parity(beam_isotope)

    #get beam energy
    user_energy = get_user_beam_energy()
    
    #if a reaction other than (d,p) is wanted, these next sections shouuld be edited.
    
    #we also need to get the deuteron
    target = Isotope(2,'H',mass_df)
    target.spin = 1
    target.parity = 1

    #define our ejectile (proton)
    ejectile = Isotope(1,'H',mass_df)
    ejectile.spin = 0.5
    ejectile.parity = 1
    
    
    #calculate our binding energy of the target
    target.binding_energy = calculate_deuteron_binding_energy(mass_df)

    
    #create the states in the final nucleus here
    num_states = get_user_number_states()
    final_states = []
    for _ in range(num_states):
         #calculate our recoil
        recoil = create_recoil(beam_isotope,target,ejectile,mass_df)
        get_user_excited_state(recoil)
        calculate_q_value(beam_isotope,target,ejectile,recoil)
        calculate_L_transfer(beam_isotope,target,ejectile,recoil)

        transferred_part = calculate_transferred_particle(beam_isotope,recoil,mass_df)
        
        calculate_binding_energy(recoil,transferred_part,mass_df)
        get_user_orbital(recoil)
        calculate_number_nodes(recoil)
        final_states.append(recoil)


    #starting construction of the FRESCO file here
    #this is the part that is not read by FRESCO, it is for the user's benefit
    fresco_string = f' {beam_isotope.isotope}(d,p){recoil.isotope} at {user_energy} MeV in inverse kinematics'

    #add the header that starts the FRESCO initialization
    fresco_string += '\n' + construct_fresco_header(user_energy)
    #add the first partition for the beam and target
    fresco_string += '\n\n' + construct_partition(beam_isotope,target,beam_isotope,1)#only one state for the beam and target
    #we use beam_isotope both times so that the q-value is 0 for the beam (which it should be because there is no reaction)

    #construct the intial state for the beam+target
    fresco_string+='\n' + construct_states(beam_isotope,target,recoil)

    #now construct the final states
    fresco_string +='\n\n'+construct_partition(recoil,ejectile,recoil,num_states)
    for i in range(num_states):
        if (i > 0):
            fresco_string += '\n '
        else:
            fresco_string += '\n'
            
        fresco_string +=construct_states(final_states[i],ejectile,final_states[i])
   
    fresco_string += '\n&partition /'
    #end of partition here

    
    #potentials here

    #initialize our potentials first:
    neut_pot = NeutronPotential()
    neut_pot.InitializeDependentParams(beam_isotope.A,user_energy)

    prot_pot = ProtonPotential() #beam with proton
    deut_pot = DeuteronPotential() #beam with deuteron
    prot_recoil_pot = ProtonPotential() #recoil with proton

    #determine what potentials to use
    determine_neutron_potential() #currently doesn't do anything.

    #proton:
    ppot = determine_proton_potential()
    if ('P' == ppot):
        prot_pot.PPotential(beam_isotope.A,beam_isotope.Z,user_energy)
        prot_recoil_pot.PPotential(recoil.A,recoil.Z,user_energy)
    else:
        prot_pot.BGPotential(beam_isotope.A,beam_isotope.Z,user_energy)
        prot_recoil_pot.BGPotential(recoil.A,recoil.Z,user_energy)
    #deuteron:
    dpot = determine_deuteron_potential()
    if ('Daehnick' == dpot):
        deut_pot.DPotential(beam_isotope.A,beam_isotope.Z,user_energy)
        
    else:
        deut_pot.LHPotential(beam_isotope.A,beam_isotope.Z,user_energy)
    
    #beam+deuteron potential
    fresco_string += '\n\n' + construct_potential(beam_isotope,deut_pot,user_energy,1)

    #beam+proton:
    fresco_string += '\n\n' + construct_potential(beam_isotope,prot_pot,user_energy,2)

    #beam+neutron:
    fresco_string += '\n\n' + construct_potential(beam_isotope,neut_pot,user_energy,3)

    #standard deuteron potential
    fresco_string += '\n\n' + construct_deuteron_potential()

    #recoil+proton:
    fresco_string += '\n\n' + construct_potential(recoil,prot_recoil_pot,user_energy,5)

    fresco_string += '\n\n &pot /'
    #end of potentials here

    
    #overlap here

    #overlap of deuteron first:
    fresco_string += '\n\n\n' + construct_overlap(target,"")

    for i in range(len(final_states)):
        fresco_string += '\n  ' + construct_overlap(final_states[i],str(i+1))

    fresco_string +='\n &overlap /'
    #end of overlap
    
    #coupling info here
    #coupling header
    fresco_string +='\n\n' + construct_coupling()
    
    #deuteron coupling
    fresco_string += "\n" + construct_cfp("")
    #other state couplings
    for i in range(len(final_states)):
        fresco_string += '\n ' + construct_cfp(str(i+1)) + ' ' 
    

    fresco_string +=  '\n\n&cfp /\n\n&coupling\n\n'

    #end of coupling


    #end of construction of file. Save it now
    file_name = f'outputs/{beam_isotope.isotope}_dp_{recoil.isotope}_{dpot}_{ppot}_{int(user_energy)}_MeV.in'
    out_file = open(file_name,'w')
    out_file.write(fresco_string)
    out_file.close()


    
    print(f'\nFile written as {file_name}')

    print('\n\nEnd of program!\n\n')


    return