#isotope class and associated functions

#atomic element abbreviation
atomicElements = "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce P Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og".split(" ")

#user-written imports
from masses import *
from calculations import *
#from calculations import calculate_deuteron_binding_energy
from construction_functions import *
#from constructor import *
from inputs import *
from isotope import *
from potentials import *


#class for an isotope
#this will hold A,Z,El,mass, etc.
#@dataclass
class Isotope:

    def __init__(self,A,element,mass_df): #,spin = 0,parity=0,exc_energy=0,q_value = 0,L_transfer = 0,orbital_osc_shell = 0,orbital_orbital = 's',orbital_L=0,orbital_J=0,nn = 0,binding_energy = 0):
        self.A = A
        self.element = element

        #fill in these automatically
        self.get_proton_number()
        self.get_mass(mass_df)
        self.get_mass_amu()
        self.get_isotope()
        
        #fill in these with default 0 for everything
        self.spin = 0
        self.parity = 0
        self.exc_energy = 0
        self.q_value = 0
        self.L_transfer = 0 #L transfer to this state (in the case of this being the recoil)
        #associated orbital info for a recoil nucleus only
        self.orbital_osc_shell = 0 #major oscillator shell of orbital being transferred into
        self.orbital_orbital = 0 #orbital name (s, p, d, f, etc) of orbital being transferred into
        self.orbital_L = 's' #angular momentum associated with the orbital being transferred into
        self.orbital_J = 0
        self.nn = 0 #number of nodes
        self.binding_energy = 0
        

    
    
    #automatic calculations and traits here
    def get_proton_number(self):
        if "n" == self.element:
            self.Z = 0
        else:
            self.Z = atomicElements.index(self.element)+1
        
    def get_mass(self,mass_df):
        try:
            mass = float(mass_df[(mass_df['EL']== self.element) & (mass_df['A'] == self.A)]['Atomic Mass (MeV)'].iloc[0])
        except:
            self.mass = 0
        else:
            self.mass = mass
    def get_mass_amu(self):
        try:
            mass_amu = self.mass / 931.5
        except:
            self.mass_amu = 0
        else:
            self.mass_amu = mass_amu

    def get_isotope(self):
        self.isotope = str(self.A)+str(self.element)


    
    def __str__(self):
        return f'''Isotope: {self.isotope}\nA: {self.A}\nElement: {self.element}\nZ: {self.Z}\nMass (MeV): {round(self.mass,3)}
        \rMass (amu): {round(self.mass_amu,3)}\nJ: {self.spin}\nParity: {self.parity}\nExc. energy (MeV): {self.exc_energy}
        \rQ-value (MeV): {self.q_value}\nL-transfer: {self.L_transfer}\nOrbital shell: {self.orbital_osc_shell}
        \rOrbital orbital: {self.orbital_orbital}\nOrbital L: {self.orbital_L}\nOrbital J: {self.orbital_J}\nNn: {self.nn}
        \rBinding energy (MeV): {round(self.binding_energy,3)}'''
    