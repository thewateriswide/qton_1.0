# qton
A slight Python3 package for a quantum simulator based on quantum circuit model.

With Qton you can easily access more than 10 virtual qubits on your laptop.   It's also used for demonstrating how a simulator is constructed.  Thus,  making modification and adding useful features are encouraged.  For example, you can add a module for studying readout noise.  

An efficient simulation need extra skills.  Imagine a qubit gate acts on a two-qubit system,  this can be represented by a $4\times 4$ matrix.  But for a $16$-qubit system,  the size is $65536\times 65536$,  which cause memory fault for most PCs.  Actually, this strategy is bad and wasting the advantage of the gate design.  

With a closer look,  the gate matrix is extremely sparse.  Therefore,  using some linear algebra knowledge can reduce the cost.  Qton is based on this idea.  It groups gates by number of qubits it acts,  so in each group they share some optimization.  With two different groups,  any quantum processes can be realized,  in principle.  

Another idea of Qton is immediately effecting user's every request,  this simplifies the coding work and improves the readability.  But this increases the difficulty of writing fancy functions.  Another thing need to know is Qton only contains a few schoolbook style logic gates,  no advanced functions either.

## Install
Place the 'qton' folder under your Python working directory,  then you can import it as a normal package.

## Package Requirement
numpy

## _About quantum computer_
Essentially, a quantum computer is just a physical system completely characterized by a complex vector,  named as the state vector.  An event is viewed as  a transform on it,  which leaves the norm unchanged.  An observation makes the state randomly collapses to some characteristic vector determined by the observation mode.  

A quantum computer in reality needs precise control of the interaction from the environment.  It's usually quite difficult in technique.  But we can simulate it with program easily.  And simulating it helps learners to have a glimpse of the design of hardware, since they share some intrinsic properties. 
