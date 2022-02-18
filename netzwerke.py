from sympy import * #Poly, degree, fraction, symbols, simplify, factor, mathematica_code, solve, solveset, Eq, sqrt
from sympy.parsing.sympy_parser import parse_expr
import copy

class ZAdd(Add):
    #Parallele "Addition" Definieren
    def __or__(self,other):
        return ZPow(ZAdd(ZPow(self,Integer(-1)),ZPow(other,Integer(-1))),Integer(-1),evaluate=False)
    def __ror__(self,other):
        return ZPow(ZAdd(ZPow(self,Integer(-1)),ZPow(other,Integer(-1))),Integer(-1),evaluate=False)
class ZPow(Pow):
    #Parallele "Addition" Definieren
    def __or__(self,other):
        return ZPow(ZAdd(ZPow(self,Integer(-1)),ZPow(other,Integer(-1))),Integer(-1),evaluate=False)
    def __ror__(self,other):
        return ZPow(ZAdd(ZPow(self,Integer(-1)),ZPow(other,Integer(-1))),Integer(-1),evaluate=False)
class ZMul(Mul):
    #Parallele "Addition" Definieren
    def __or__(self,other):
        return ZPow(ZAdd(ZPow(self,Integer(-1)),ZPow(other,Integer(-1))),Integer(-1),evaluate=False)
    def __ror__(self,other):
        return ZPow(ZAdd(ZPow(self,Integer(-1)),ZPow(other,Integer(-1))),Integer(-1),evaluate=False)
class Z(Symbol):
    #Parallele "Addition" Definieren
    def __or__(self,other):
        return ZPow(ZAdd(ZPow(self,Integer(-1)),ZPow(other,Integer(-1))),Integer(-1),evaluate=False)
    def __ror__(self,other):
        return ZPow(ZAdd(ZPow(self,Integer(-1)),ZPow(other,Integer(-1))),Integer(-1),evaluate=False)

class R:
    def __new__(cls,name):
        globals()[f"R{name}"] = Z("R"+name)
        globals()[f"R{name}"] = globals()[f"R{name}"]
        return globals()[f"R{name}"]
class L:
    def __new__(cls,name):
        globals()[f"L{name}"] = Z("L"+name)
        globals()[f"L{name}"] = ZMul(globals()[f"L{name}"],s)
        return globals()[f"L{name}"]
class C:
    def __new__(cls,name):
        globals()[f"C{name}"] = Z("C"+name)
        globals()[f"C{name}"] = ZPow(ZMul(globals()[f"C{name}"],s),Integer(-1),evaluate=False)
        return globals()[f"C{name}"]

#Programm
s = Z('s') 

#Bauteile instanziieren
ZLh = L('h') # ZLx -> sLx
ZCh = C('h') # ZCx -> 1/(sCx)
ZRs = R('s') # ZR  -> R

Zteil = (ZLh|ZCh)
Zges = ZRs+(ZLh|ZCh)

print("Zteil/Zges = " + str(mathematica_code(simplify(factor(Zteil/Zges)))))
