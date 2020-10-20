'''
Basic quantum operations and corresponding unitaries. 

Each gate is expressed as a matrix in the minimal state space it acts.
We follow the convention in most textbooks, for example, Nielsen and Chuang's.
'''

__all__ = [
    'h_gate', 
    'x_gate',
    'y_gate',
    'z_gate',
    's_gate',
    't_gate',
    'rx_gate',
    'ry_gate',
    'rz_gate',
    'ch_gate',
    'cx_gate',
    'cy_gate',
    'cz_gate',
    'sw_gate',
    'crx_gate',
    'cry_gate',
    'crz_gate',
    ]

from numpy import array, sqrt, sin, cos, exp

# Fixed single-qubit gates.
h_gate = array([[1, 1], [1, -1]]) * sqrt(0.5)
x_gate = array([[0, 1], [1, 0]])
y_gate = array([[0, -1j], [1j, 0]])
z_gate = array([[1, 0], [0, -1]])
s_gate = array([[1, 0], [0, 1j]])
t_gate = array([[1, 0], [0, (1+1j) * sqrt(0.5)]])

# Single-qubit gates with parameters.
def rx_gate(theta):
    t = theta * 0.50
    return array([
        [cos(t), -1j * sin(t)], 
        [-1j * sin(t), cos(t)],
        ])
                      
def ry_gate(theta):
    t = theta * 0.50
    return array([
        [cos(t), -sin(t)], 
        [sin(t),  cos(t)],
        ])

def rz_gate(theta):
    t = theta * 0.50
    return array([
        [exp(-1j*t), 0], 
        [0,  exp(1j*t)],
        ])                     

# Fixed two-qubit gates
ch_gate = array([
    [1, 0, 0, 0], 
    [0, 1, 0, 0], 
    [0, 0, sqrt(0.5), sqrt(0.5)],
    [0, 0, sqrt(0.5),-sqrt(0.5)],
    ])
cx_gate = array([
    [1, 0, 0, 0], 
    [0, 1, 0, 0], 
    [0, 0, 0, 1], 
    [0, 0, 1, 0],
    ])
cy_gate = array([
    [1, 0, 0, 0], 
    [0, 1, 0, 0], 
    [0, 0, 0, -1j], 
    [0, 0, 1j, 0],
    ])
cz_gate = array([
    [1, 0, 0, 0], 
    [0, 1, 0, 0], 
    [0, 0, 1, 0], 
    [0, 0, 0, -1],
    ])
sw_gate = array([
    [1, 0, 0, 0], 
    [0, 0, 1, 0], 
    [0, 1, 0, 0], 
    [0, 0, 0, 1],
    ])

# Two-qubit gates with parameters.
def crx_gate(theta):
    t = theta * 0.50
    return array([
        [1, 0, 0, 0], 
        [0, 1, 0, 0],
        [0, 0, cos(t), -1j*sin(t)], 
        [0, 0, -1j*sin(t), cos(t)],
        ])
                      
def cry_gate(theta):
    t = theta * 0.50
    return array([
        [1, 0, 0, 0], 
        [0, 1, 0, 0],
        [0, 0, cos(t), -sin(t)], 
        [0, 0, sin(t),  cos(t)],
        ])

def crz_gate(theta):
    t = theta * 0.50
    return array([
        [1, 0, 0, 0], 
        [0, 1, 0, 0],   
        [0, 0, exp(-1j*t), 0], 
        [0, 0, 0,  exp(1j*t)],
        ])