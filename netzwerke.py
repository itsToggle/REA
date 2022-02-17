from sympy import * #Poly, degree, fraction, symbols, simplify, factor, mathematica_code, solve, solveset, Eq, sqrt
from sympy.parsing.sympy_parser import parse_expr
import copy

#Parallele "Addition" Definieren
def parallel(self,other):
    return 1/(1/self+1/other)
Mul_or = Mul.__or__
Mul.__or__ = parallel
Mul_ror = Mul.__ror__
Mul.__ror__ = parallel
Symbol_or = Symbol.__or__
Symbol.__or__ = parallel
Symbol_ror = Symbol.__ror__
Symbol.__ror__ = parallel

s = symbols('s')

#Bauteile
class R:
    def __new__(cls,name):
        globals()[f"R{name}"] = symbols("R"+name)
        globals()[f"R{name}"] = globals()[f"R{name}"]
        return globals()[f"R{name}"]
class L:
    def __new__(cls,name):
        globals()[f"L{name}"] = symbols("L"+name)
        globals()[f"L{name}"] = s*globals()[f"L{name}"]
        return globals()[f"L{name}"]
class C:
    def __new__(cls,name):
        globals()[f"C{name}"] = symbols("C"+name)
        globals()[f"C{name}"] = 1/(s*globals()[f"C{name}"])
        return globals()[f"C{name}"]

#Programm
j = symbols('j')
w = symbols('w')
s = j*w

#Bauteile instanziieren
Lh = L('h') # Lx -> sLx
Ch = C('h') # Cx -> 1/(sCx)
Rs = R('s') # R  -> R

Zges = Rs+(Lh|Ch)
Zteil = Lh|Ch

print("Zteil/Zges = " + str(mathematica_code(simplify(factor(Zteil/Zges)))))
