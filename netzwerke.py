from sympy import * #Poly, degree, fraction, symbols, simplify, factor, mathematica_code, solve, solveset, Eq, sqrt
from sympy.parsing.sympy_parser import parse_expr
import copy

class Z(Symbol):
    #Parallele "Addition" Definieren
    def __or__(self,other):
        return 1/(1/self+1/other)
    def __ror__(self,other):
        return 1/(1/self+1/other)

Mul.__or__ = Z.__or__ 
Mul.__ror__ = Z.__ror__ 

class R:
    def __new__(cls,name):
        globals()[f"R{name}"] = Z("R"+name)
        globals()[f"R{name}"] = globals()[f"R{name}"]
        return globals()[f"R{name}"]
class L:
    def __new__(cls,name):
        globals()[f"L{name}"] = Z("L"+name)
        globals()[f"L{name}"] = s*globals()[f"L{name}"]
        return globals()[f"L{name}"]
class C:
    def __new__(cls,name):
        globals()[f"C{name}"] = Z("C"+name)
        globals()[f"C{name}"] = 1/(s*globals()[f"C{name}"])
        return globals()[f"C{name}"]

#Programm
s = Z('s') 
j = Z('j')
w = Z('w')
s = j*w

#Bauteile instanziieren
Lh = L('h') # Lx -> sLx
Ch = C('h') # Cx -> 1/(sCx)
Rs = R('s') # R  -> R

Zteil = Lh|Ch
Zges = Rs+(Lh|Ch)

print("Zteil/Zges = " + str(mathematica_code(simplify(factor(Zteil/Zges)))))
