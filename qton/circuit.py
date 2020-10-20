'''
Class for quantum circuit model.
'''

__all__ = ['Circuit']

from numpy import array, zeros, abs, matmul, conj, arange
from numpy.random import choice

from .gate import *

class Circuit(object):
    '''Class for simulating a quantum computer.

    Quantum computer here means a quantum circuit model.  The basis convention 
    we use is same as most textbooks.  Which means the 0th qubit is the 
    leftmost one in a basis like |10...00>.

    Example:

        To create an instance:
            cir = Circuit(number_of_qubits)
        To use the number of qubits:
            cir.number_of_qubits
        To apply an operation:
            cir.cx(0, 1)
        Here, the qubits are indexed by integers.
        To use the instance's state:
            cir.state
        To return a measurement:
            observe = cir.measure()
    '''
    
    def __init__(self, number_of_qubits):
        '''Create a circuit object. 

        By default, the sate starts with all qubits are up under Z basis.

        -IN:
            number_of_qubits --- number of qubits in the circuit.
                type: integer

        -INFLUENCED:
            self.number_of_qubits --- number of qubits in the circuit.
                type: integer
            self.state --- state of the circuit.
                type: 1 dimensin numpy.array of complex.
        '''
        self.number_of_qubits = number_of_qubits
        self.state = zeros(2**number_of_qubits, complex)
        self.state[0] = 1.0
        return None
    
    def initialize(self, vector):
        '''Initialize the circuit state with a given vector.

        The vector must be normalized already.

        -IN:
            vector --- a normalized state.
                type: 1 dimensin numpy.array of complex.

        -INFLUENCED:
            self.state --- state of the circuit.
                type: 1 dimensin numpy.array of complex.
        '''
        self.state = array(vector, complex)
        return None
                                    
    def measure(self):
        '''Do a measurement on the circuit. 

        This returns a certain basis' ID number according to the probability 
        associated with self.state. For example, 

            1 

        means the basis |01> on a two-qubit circuit.

        To simplify the simulation, this measurement leaves the circuit state
        unaffected.

        -RETURN:
            --- basis ID.
                type: integer
        '''
        prob = zeros(2**self.number_of_qubits)
        for i in range(2**self.number_of_qubits):
            prob[i] = abs(self.state[i])**2
        return choice(arange(2**self.number_of_qubits), p = prob)

    def swap(self, q1, q2):
        '''Swap any two qubits in the circuit. 

        This operation is a groundstone for other operations.  On some real 
        device, the swap function also plays a crucial role.

        Note, if the two qubit arguments are same, nothing will be implemented.

        The concept of the algorithm is to swap any two bases like

            |...b[q1]...b[q2]...> 
        
        and 
        
            |...b[q2]...b[q1]...>

        -IN:
            q1 --- the index of the qubit to swap.
                type: integer
            q2 --- the index of the other qubit to swap.
                type: integer

        -INFLUENCED:
            self.state --- state of the circuit.
                type: 1 dimensin numpy.array of complex.
        '''
        if q1 == q2: return None
        old_state = self.state.copy()
        form = '0%db' % self.number_of_qubits
        for i in range(2**self.number_of_qubits):
            bit_string = format(i, form)
            if bit_string[q1] != bit_string[q2]:
                bit_list = list(bit_string)
                tmp = bit_list[q1]  # Switch the value by tmp.
                bit_list[q1] = bit_list[q2]
                bit_list[q2] = tmp
                j = int(''.join(bit_list), 2)
                self.state[i] = old_state[j]
        return None
        
    def _single_gate(self, op, targ):
        '''Act a single-qubit gate on an arbitray qubit. 

        The target qubit will be swapped with the last qubit before and after 
        the action.  The target could be a sequence of qubit indices. 

        This is an internal function based on swap() function. 

        -IN:
            op --- single-qubit gate or operation.
                type: 2 by 2 numpy.array.
            targ --- index of the target qubit.
                type: integer or sequence of integers.

        -INFLUENCED:
            self.state --- state of the circuit.
                type: 1 dimensin numpy.array of complex.
        '''
        if type(targ) is int:
            targ = [targ]
        else:
            targ = list(set(targ))

        for i in targ:
            # the last qubit is used as a processor.
            self.swap(i, self.number_of_qubits-1)
            for idx in range(0, 2**self.number_of_qubits, 2):
                self.state[idx:idx+2] = matmul(op, self.state[idx : idx+2])
            self.swap(i, self.number_of_qubits-1)
        return None
 
    def _double_gate(self, op, ctrl, targ):
        '''Act a two-qubit gate on two arbitray qubits. 

        The two qubits are labelled as control and target. This is also based 
        on swap() function.

        The concept of the algorithm is to swap the two qubits with the last
        two before and after applying the operation. The last two qubits are 
        used as a processor. Therefore, the swap process is the key.

        This is an internal function and a basic for other double qubit 
        operation. to reduce the complexity, ctrl and targ CANNOT be sequence
        type.

        -IN:
            op --- Double-qubit gate or operation.
                type: 4 by 4 numpy.array.
            ctrl --- index of the control qubit.
                type: integer
            targ --- index of the target qubit.
                type: integer

        -INFLUENCED:
            self.state --- state of the circuit.
                type: 1 dimensin numpy.array of complex.
        '''
        if ctrl == targ: 
            raise Exception    # control and target can't be same.

        # last two qubits are used as a processor or registers.
        reg = {self.number_of_qubits-2, self.number_of_qubits-1}
        if ctrl not in reg and targ not in reg:
            self.swap(ctrl, self.number_of_qubits-2)
            self.swap(targ, self.number_of_qubits-1)
            for idx in range(0, 2**self.number_of_qubits, 4):
                self.state[idx:idx+4] = matmul(op, self.state[idx:idx+4])
            self.swap(targ, self.number_of_qubits-1)
            self.swap(ctrl, self.number_of_qubits-2)
        elif ctrl in reg and targ in reg:
            if ctrl == self.number_of_qubits-1: self.swap(ctrl, targ)
            for idx in range(0, 2**self.number_of_qubits, 4):
                self.state[idx:idx+4] = matmul(op, self.state[idx:idx+4])
            if ctrl == self.number_of_qubits-1: self.swap(ctrl, targ)
        elif ctrl in reg and targ not in reg:
            if ctrl == self.number_of_qubits-1: self.swap(ctrl, self.number_of_qubits-2)
            self.swap(targ, self.number_of_qubits-1)
            for idx in range(0,2**self.number_of_qubits,4):
                self.state[idx:idx+4] = matmul(op, self.state[idx:idx+4])
            self.swap(targ, self.number_of_qubits-1)
            if ctrl == self.number_of_qubits-1: self.swap(ctrl, self.number_of_qubits-2)
        elif ctrl not in reg and targ in reg:
            if targ == self.number_of_qubits-2: self.swap(targ, self.number_of_qubits-1)
            self.swap(ctrl, self.number_of_qubits-2)
            for idx in range(0, 2**self.number_of_qubits, 4):
                self.state[idx:idx+4] = matmul(op, self.state[idx:idx+4])
            self.swap(ctrl, self.number_of_qubits-2)
            if targ == self.number_of_qubits-2: self.swap(targ, self.number_of_qubits-1)    
        return None   

# 
# All other operations are based on _single_gate or _double_gate functions. 
# It's easy to add more methods in future by this way.
# 

    def h(self, targ):
        '''Hadamard operation.

        Circuit.h(targ)
        '''
        self._single_gate(h_gate, targ)
    
    def x(self, targ):
        '''Pauli X operation.

        Circuit.x(targ)
        '''
        self._single_gate(x_gate, targ)
    
    def y(self, targ):
        '''Pauli Y operation.

        Circuit.y(targ)
        '''
        self._single_gate(y_gate, targ)
    
    def z(self, targ):
        '''Pauli Z operation.

        Circuit.z(targ)
        '''
        self._single_gate(z_gate, targ)
        
    def s(self, targ):
        '''Phase S operation.

        Circuit.s(targ)
        '''
        self._single_gate(s_gate, targ)
        
    def sdg(self, targ):
        '''S Dagger operation.

        Circuit.sdg(targ)
        '''
        self._single_gate(conj(s_gate).T, targ)
        
    def t(self, targ):
        '''pi/8 T operation.

        Circuit.t(targ)
        '''
        self._single_gate(t_gate, targ)
        
    def tdg(self, targ):
        '''T Dagger operation.

        Circuit.tdg(targ)
        '''
        self._single_gate(conj(t_gate).T, targ)
        
    def rx(self, theta, targ):
        '''Rotation along X axis.

        Circuit.rx(theta, targ)
        '''
        self._single_gate(rx_gate(theta), targ)

    def ry(self, theta, targ):
        '''Rotation along Y axis.

        Circuit.ry(theta, targ)
        '''
        self._single_gate(ry_gate(theta), targ)
        
    def rz(self, theta, targ):
        '''Rotation along Z axis.

        Circuit.rz(theta, targ)
        '''
        self._single_gate(rz_gate(theta), targ)  

     
    def ch(self, ctrl, targ):
        '''Controlled hadamard operation.

        Circuit.ch(ctrl, targ)
        '''
        self._double_gate(ch_gate, ctrl, targ)
                        
    def cx(self, ctrl, targ):
        '''Controlled Pauli X operation, or CNOT operation.

        Circuit.cx(ctrl, targ)
        '''
        self._double_gate(cx_gate, ctrl, targ)

    def cy(self, ctrl, targ):
        '''Controlled Pauli Y operation.

        Circuit.cy(ctrl, targ)
        '''
        self._double_gate(cy_gate, ctrl, targ)

    def cz(self, ctrl, targ):
        '''Controlled Pauli Z operation.

        Circuit.cz(ctrl, targ)
        '''
        self._double_gate(cz_gate, ctrl, targ)
        
    def crx(self, theta, ctrl, targ):
        '''Controlled rotation along X axis.

        Circuit.crx(ctrl, targ)
        '''
        self._double_gate(crx_gate(theta), ctrl, targ)

    def cry(self, theta, ctrl, targ):
        '''Controlled rotation along Y axis.

        Circuit.cry(ctrl, targ)
        '''
        self._double_gate(cry_gate(theta), ctrl, targ)

    def crz(self, theta, ctrl, targ):
        '''Controlled rotation along Z axis.
        
        Circuit.crz(ctrl, targ)
        '''
        self._double_gate(crz_gate(theta), ctrl, targ)
