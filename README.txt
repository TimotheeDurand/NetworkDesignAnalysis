Both algorithm were developped using Python 3 (version 3.6.8).

The python libraries required are:
- networkx (https://networkx.github.io/documentation/)
- numpy (https://www.numpy.org/)

They can be installed using pip:
pip3 install networkx
pip3 install numpy

For more information, please visit [https://networkx.github.io/documentation/stable/install.html] and [https://www.scipy.org/install.html]


INDEPENDANT CASCADE

The implementation of the Independant Cascade can be found in the "IndependantCascade" Folder:
To test out the algorithm, the following command has to be run:

python3 main.py

By default, it will run the Independant Cascade on the 'Wiki-Vote.txt' instance (https://snap.stanford.edu/data/wiki-Vote.html). 

It is possible to test it on another instance by modifying the 'main.py' file directly (line 17). However, the other instances (test_graph_XX.txt) where only intended to be used for testing purposes.



DUAL ASCENT

The implementation of the Dual Ascent can be found in the "DualAscent" Folder:
To test out the algorithm, the following command has to be run:

python3 main.py

By default it will run the algorithm on the './testfiles/B18.stp' file. A lot of different instances can be tested, and they are stored in the 'testfiles' folder. All of them are retrieved from the SteilLib website (http://steinlib.zib.de/). The file 'instancesinfo.csv' contains information about instances such as their size, their complexity and the expected optimal value.