import numpy as np
import matplotlib as mp
import math as m

def ceil(value, prefix):
    """This function rounds values up to the nearest integer with regards to an SI prefix"""
    return 10**(prefix)*(m.ceil(value*10**(-prefix)))

def buckling_diameter(compressive_force, length, safety_factor, youngs_modulus, end_conditions):
    return 2*((2*safety_factor*compressive_force*length**2)/(end_conditions*m.pi**3*youngs_modulus))**(1/4)

# Safety factor

N = 2.5

# Material constants

E_AL = 69*10**9
E_ST = 180*10**9

RHO_AL = 2700
RHO_ST = 7900

YIELD_STRENGTH_AL = 95*10**6
YIELD_STRENGTH_ST = 502*10**6

SHEAR_STRENGTH_AL = 0.5*YIELD_STRENGTH_AL
SHEAR_STRENGTH_ST = 0.5*YIELD_STRENGTH_ST

ALLOW_AL = YIELD_STRENGTH_AL/N
ALLOW_SHEAR_AL = SHEAR_STRENGTH_AL/N

ALLOW_ST = YIELD_STRENGTH_ST/N
ALLOW_SHEAR_ST = SHEAR_STRENGTH_ST/N

# Known values

LOAD = 7.5*10**3                                                # Given
LINK_LENGTH = 181*10**(-3)                                      # Obtained with Geometrical Analysis
THETA_MIN = m.radians(26.23)                                    # Design decision
THETA_MAX = m.radians(75.21)                                    # Design decision
LINK_DIAMETER = 11*10**(-3)                                     # Obtained through buckling criteria for a single link
LINK_CROSS_SECTIONAL_AREA = LINK_DIAMETER**2*m.pi/4
LINK_AREA_MOMENT_OF_INERTIA = m.pi*LINK_DIAMETER**4/64

# Calculated link values

LINK_MAX_COMPRESSIVE_FORCE = LOAD/(2*m.sin(THETA_MIN))
LINK_BUCKLING_FORCE = m.pi**2*E_AL*LINK_AREA_MOMENT_OF_INERTIA/(LINK_LENGTH**2)

# Calculated bolt values 

BOLT_ALLOW_SHEAR = SHEAR_STRENGTH_ST/N
BOLT_DIAMETER = ceil(m.sqrt(4*LINK_MAX_COMPRESSIVE_FORCE/(m.pi*BOLT_ALLOW_SHEAR)),-3)

# Related link values

LINK_END_WIDTH = ceil(LINK_MAX_COMPRESSIVE_FORCE*m.cos(THETA_MIN)/(BOLT_DIAMETER*ALLOW_AL), -3)

# print(BOLT_DIAMETER)
# print(LINK_END_WIDTH)

print('Design decision: Two links will be fastened to a single cylindrical nut for power screw')
print('Consequently, each link bears the load {:.2f}kN'.format(LINK_MAX_COMPRESSIVE_FORCE/2000))

LINK_DIAMETER_2 = ceil(buckling_diameter(LINK_MAX_COMPRESSIVE_FORCE/2, LINK_LENGTH, N, E_AL, 1),-3)

print('Buckling diameter of each link is {:.2f}mm'.format(LINK_DIAMETER_2*1000))

POWER_SCREW_TENSILE_FORCE = 2*LOAD*m.cos(THETA_MIN)/m.sin(THETA_MIN)
BOLT_MAX_SHEAR_FORCE = POWER_SCREW_TENSILE_FORCE/2
BOLT_DIAMETER_2 = ceil(m.sqrt(4*BOLT_MAX_SHEAR_FORCE/(m.pi*ALLOW_SHEAR_ST)),-3)

print('Maximum shear force between links and nut is {:.2f}kN'.format(BOLT_MAX_SHEAR_FORCE/1000))
print('Consequently, the bolt diameter must be at least {:.2f}mm'.format(BOLT_DIAMETER_2*1000))

LINK_END_WIDTH_2 = ceil(LINK_MAX_COMPRESSIVE_FORCE/2*m.cos(THETA_MIN)/(BOLT_DIAMETER_2*ALLOW_AL), -3)

print('Due to bearing stress the link must have an end width of at least {:.2f}mm'.format(LINK_END_WIDTH_2*1000))
print('The nut/bolt length is larger than {:.2f}mm'.format(4*LINK_END_WIDTH_2*1000+15))

LINK_END_HEIGHT_2 = 0.03                                            # Design decision
