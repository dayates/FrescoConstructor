#optical potentials

#user-written imports
from masses import *
from constructors.calculations import *
#from calculations import calculate_deuteron_binding_energy
from constructors.construction_functions import *
#from constructor import *
from constructors.inputs import *
from constructors.isotope import *
from constructors.potentials import *

#determine the potentials to use:
def determine_neutron_potential():
    #no option right now. Just return the potential

    user_pot = "WH"
    print(f'Using neutron potential {user_pot}')
    
    return "WH" #Wilmore and Hodgson potential

def determine_proton_potential():
    #BG or Perey potentials. Default is "BG"
    possible_potentials = [["BG","Becchetti and Greenlees"],["P","Perey"]]
    
    print("Possible proton potentials:")
    for p,name in possible_potentials:
        print(f'{p}\t- {name}')
    
    user_pot = input("Enter the proton potential (default BG): ")

    if user_pot not in (pot[0] for pot in possible_potentials):
        user_pot = 'BG'

    print(f'Using proton potential {user_pot}')

    return user_pot

def determine_deuteron_potential():
    #LH or Daehnick potentials. Default is LH
    possible_potentials = [["LH","Lohr and Haebleri"],["D","Daehnick"]]

    print("Possible deuteron potentials:")
    for p,name in possible_potentials:
        print(f'{p}\t- {name}')

    user_pot = input("Enter the deuteron potential (default LH): ")

    if user_pot not in (pot[0] for pot in possible_potentials):
        user_pot = 'LH'

    print(f'Using deuteron potential {user_pot}')

    return user_pot



#class definitions here

#this will define the neutron potential
class NeutronPotential():
    # neutron potential of Wilmore and Hodgson
    # D. Wilmore and P.E. Hodgson, Nuclear Physics 55:673-694 (1964).
    # https://doi.org/10.1016/0029-5582(64)90184-1

    def __init__(self):
        self.A0 = 0.66
        self.AD = 0.48
        self.RC = 0 #no coulomb radius for neutron
        #these all get initalized in InitializeDependentParams()
        self.V0 = 0
        self.R0 = 0
        self.WD = 0
        self.RD = 0

    
    def InitializeDependentParams(self,A,E): #mass number A, lab inverse kinematics energy E
        #convert from lab inverse kinematics lab energy into normal kinematics lab energy
        #energy is Elab (heavy) * (mass light)/(mass heavy)
        #since this is a neutron potential, m(neutron) ~1 amu, so this will be pretty close
        E = E/A 
        #initialize our parameters based on that
        #equations 9-13
        self.V0 = 47.01 - 0.267*E - 0.00118*E**2
        self.R0 = 1.322 - A*7.6e-4 + A**2*4e-6 - A**3*8e-9
        self.WD = max(0,9.52 - 0.053*E)
        self.RD = 1.266 - A*3.7e-4 + A**2*2e-6 - A**3*4e-9

    def __str__(self):

        return f'V0: {self.V0}\nR0: {self.R0}\nA0: {self.A0}\nWD: {self.WD}\nRD: {self.RD}\nAD: {self.AD}'



#proton potential class
class ProtonPotential():


    def __init__(self):
        self.V0 = 0
        self.R0 = 0
        self.A0 = 0
        self.W0 = 0
        self.WD = 0
        self.RD = 0
        self.AD = 0
        self.VLS = 0
        self.RLS = 0
        self.ALS = 0
        self.RC = 0


    def BGPotential(self,A,Z,E): #mass number A, atomic number Z, incident lab energy (of proton beam).
        # this is the potential of Becchetti and Greenlees
        # F.D. Becchetti and G.W. Greenlees, Phys. Rev. 182:1190-1209 (1969)
        # https://doi.org/10.1103/PhysRev.182.1190
    
        #convert from lab inverse kinematics lab energy into normal kinematics lab energy
        #energy is Elab (heavy) * (mass light)/(mass heavy)
        #since this is a proton potential, m(proton) ~1 amu, so this will be pretty close
        E = E/A
        #now initialize everything else
        #equation 8
        self.V0 = 54.0 - 0.32*E + 0.4*Z/(A**(1/3)) + 24.0*(A-2*Z)/A #substituting (A-2*Z) for (N-Z) from the paper
        self.R0 = 1.17
        self.A0 = 0.75
        self.W0 = max(0,0.22*E - 2.7)
        self.WD = max(0,11.8 - 0.25*E + 12.0*(A-2*Z)/A) #substituting (A-2*Z) for (N-Z) from the paper
        self.RD = 1.32
        self.AD = 0.51 + 0.7*(A-2*Z)/A #substituting (A-2*Z) for (N-Z) from the paper
        self.VLS = 6.2
        self.RLS = 1.32
        self.ALS = 0.75
        self.RC = 1.25

    def PPotential(self,A,Z,E):
        # potential of Perey
        # F.G. Perey, Phys. Rev. 131:745-763 (1963)
        # https://doi.org/10.1103/PhysRev.131.745

        #convert from lab inverse kinematics lab energy into normal kinematics lab energy
        #energy is Elab (heavy) * (mass light)/(mass heavy)
        #since this is a proton potential, m(proton) ~1 amu, so this will be pretty close
        E = E/A
        #now initialize everything else
        #equation 2, Table 5, first paragraph in section 3, end of page 753 (possibly equation on 754)
        self.V0 = 53.3 - 0.55*E + (0.4*Z/(A**(1/3)) + 27*(A-2*Z)/A)
        self.R0 = 1.25
        self.A0 = 0.65
        self.W0 = 0
        self.WD = 13.5 #quoted as 13.5+-2.0 MeV
        self.RD = 1.25
        self.AD = 0.47
        self.VLS = 7.5
        self.RLS = 1.25
        self.ALS = 0.47
        self.RC = 1.25
        


    def __str__(self):
        return f'''V0: {self.V0}\nR0: {self.R0}\nA0: {self.A0}\nW0: {self.W0}\nWD: {self.WD}\nRD: {self.RD}\nAD: {self.AD}
            \rVLS: {self.VLS}\nRLS: {self.RLS}\nALS: {self.ALS}\nRC: {self.RC}'''
    

#deuteron potentials here
class DeuteronPotential():


    def __init__(self):
        self.V0 = 0
        self.R0 = 0
        self.A0 = 0
        self.W0 = 0
        self.WD = 0
        self.RD = 0
        self.AD = 0
        self.VLS = 0
        self.RLS = 0
        self.ALS = 0
        self.RC = 0


    def LHPotential(self,A,Z,E):
        # deuteron potential of Lohr and Haeberli
        # J.M. Lohr and W. Haeberli, Nuclear Physics A, 232(2):381-397 (1974)
        # https://doi.org/10.1016/0375-9474(74)90627-7
        
        #convert from lab inverse kinematics lab energy into normal kinematics lab energy
        #energy is Elab (heavy) * (mass light)/(mass heavy)
        #since this is a deuteron potential, m(deuteron) ~2 amu, so this will be pretty close
        E = E*2/A
        #initialize everything else now
        #Eq 1, 2, 3,
        self.V0 = 91.13 + 2.20*Z/(A**(1/3))
        self.R0 = 1.05
        self.A0 = 0.80
        self.W0 = 0
        self.WD = 218*A**(-2/3)
        self.RD = 1.43
        self.AD = 0.50 + 0.013*A**(2/3)
        self.VLS = 7.0
        self.RLS = 0.75
        self.ALS = 0.5
        self.RC = 1.3



    def DPotential(self,A,Z,E):
        # potential of Daehnick
        # W.W. Daehnick, J.D. Childs, Z. Vrcelj, Phys. Rev. C 21:2253-2274 (1980)
        # https://doi.org/10.1103/PhysRevC.21.2253

        #convert from lab inverse kinematics lab energy into normal kinematics lab energy
        #energy is Elab (heavy) * (mass light)/(mass heavy)
        #since this is a deuteron potential, m(deuteron) ~2 amu, so this will be pretty close
        E = E*2/A
        #initialize everything else now
        #Table 3, Potential "79 DCV, F"
        self.V0 = 88.0 - 0.283*E + 0.88*Z*A**(-1/3) #also called V_R sometimes
        self.R0 = 1.17
        self.A0 = 0.717 + 0.0012*E
        self.W0 = (12 + 0.031*E)*(1-np.exp(-(E/100)**2))
        self.WD = (12 + 0.031*E)*np.exp(-(E/100)**2)
        self.RD = 1.376 - 0.01*np.sqrt(E)
        self.AD = 0.52 + 0.07*A**(1/3) #this ignores the contributions from the magic number sum in this potential for now
        self.VLS = 7.20 - 0.032*E
        self.RLS = 1.07
        self.ALS = 0.66
        self.RC = 1.30

    def __str__(self):
        return f'''V0: {self.V0}\nR0: {self.R0}\nA0: {self.A0}\nW0: {self.W0}\nWD: {self.WD}\nRD: {self.RD}\nAD: {self.AD}
            \rVLS: {self.VLS}\nRLS: {self.RLS}\nALS: {self.ALS}\nRC: {self.RC}'''
