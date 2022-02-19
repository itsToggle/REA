from sympy import *

s = symbols('s')

class Z:
    def __init__(self,name,Zges=None,children=[]):
        if not Zges == None:
            self.Z = Zges
        else:
            self.Z = Symbol('Z_['+name+']')
        self.UU = Symbol('U_['+name+']')
        self.II = Symbol('I_['+name+']')
        self.UI = self.II * self.Z
        self.IU = self.UU / self.Z
        self.name = name
    def __add__(self,other):
        #Series Addition
        with evaluate(False):
            if hasattr(other,'TN'):
                children = other.TN
                for child in children:
                    child.UU = child.UU.subs(other.UU,(self.UU+other.UU)* other.Z/(self.Z + other.Z))
                    child.IU = child.IU.subs(other.UU,(self.UU+other.UU)* other.Z/(self.Z + other.Z))
                    child.II = child.II.subs(other.II,self.II)
                    child.UI = child.UI.subs(other.II,self.II)
            else:
                children = [other]
            children += [self]
            Zges = TN(self.Z + other.Z,self.UU+other.UU,self.II,children)
            self.UU = Zges.UU * self.Z/Zges.Z
            self.II = Zges.II
            self.UI = Zges.II * self.Z
            self.IU = Zges.UU / Zges.Z
            other.UU = Zges.UU * other.Z/Zges.Z
            other.II = Zges.II
            other.UI = Zges.II * other.Z
            other.IU = Zges.UU / Zges.Z
            return Zges
    def __or__(self,other):
        #Parallel Addition
        with evaluate(False):
            if hasattr(other,'TN'):
                children = other.TN
                for child in children:
                    child.UU = child.UU.subs(other.UU,self.UU)
                    child.IU = child.IU.subs(other.UU,self.UU)
                    child.II = child.II.subs(other.II,(self.II+other.II)* (1/(1/self.Z + 1/other.Z))/other.Z)
                    child.UI = child.UI.subs(other.II,(self.II+other.II)* (1/(1/self.Z + 1/other.Z))/other.Z)
            else:
                children = [other]
            children += [self]
            Zges = TN(1/(1/self.Z + 1/other.Z),self.UU,self.II+other.II,children)
            self.UU = Zges.UU 
            self.II = Zges.II * Zges.Z/self.Z
            self.UI = Zges.II * Zges.Z
            self.IU = Zges.UU / self.Z
            other.UU = Zges.UU 
            other.II = Zges.II * Zges.Z/other.Z
            other.UI = Zges.II * Zges.Z
            other.IU = Zges.UU / other.Z
            return Zges
    def U(self,mode):
        if mode in self.UU.args:
            return simplify(factor(self.II))
        elif mode in self.UI.args:
            return simplify(factor(self.IU))
    def I(self,mode):
        if mode in self.II.args:
            return simplify(factor(self.II))
        elif mode in self.IU.args:
            return simplify(factor(self.IU))
class TN:
    def __init__(self,Zges,Uges,Iges,children):
        self.Z = Zges
        self.UU = Uges
        self.II = Iges
        self.UI = self.II * self.Z
        self.IU = self.UU / self.Z
        self.TN = children
    def __add__(self,other):
        #Series Addition
        with evaluate(False):
            if hasattr(other,'TN'):
                children = other.TN
                for child in children:
                    child.UU = child.UU.subs(other.UU,(self.UU+other.UU)* other.Z/(self.Z + other.Z))
                    child.IU = child.IU.subs(other.UU,(self.UU+other.UU)* other.Z/(self.Z + other.Z))
                    child.II = child.II.subs(other.II,self.II)
                    child.UI = child.UI.subs(other.II,self.II)
            else:
                children = [other]
            for child in self.TN:
                child.UU = child.UU.subs(self.UU,(self.UU+other.UU)* self.Z/(self.Z + other.Z))
                child.IU = child.IU.subs(self.UU,(self.UU+other.UU)* self.Z/(self.Z + other.Z))
                child.II = child.II.subs(self.II,self.II)
                child.UI = child.UI.subs(self.II,self.II)
            children += self.TN
            Zges = TN(self.Z + other.Z,self.UU+other.UU,self.II,children)
            self.UU = Zges.UU * self.Z/Zges.Z
            self.II = Zges.II
            self.UI = Zges.II * self.Z
            self.IU = Zges.UU / Zges.Z
            other.UU = Zges.UU * other.Z/Zges.Z
            other.II = Zges.II
            other.UI = Zges.II * other.Z
            other.IU = Zges.UU / Zges.Z
            return Zges
    def __or__(self,other):
        #Parallel Addition
        with evaluate(False):
            if hasattr(other,'TN'):
                children = other.TN
                for child in children:
                    child.UU = child.UU.subs(other.UU,self.UU)
                    child.IU = child.IU.subs(other.UU,self.UU)
                    child.II = child.II.subs(other.II,(self.II+other.II)* (1/(1/self.Z + 1/other.Z))/other.Z)
                    child.UI = child.UI.subs(other.II,(self.II+other.II)* (1/(1/self.Z + 1/other.Z))/other.Z)
            else:
                children = [other]
            for child in self.TN:
                child.UU = child.UU.subs(self.UU,self.UU)
                child.IU = child.IU.subs(self.UU,self.UU)
                child.II = child.II.subs(self.II,(self.II+other.II)* (1/(1/self.Z + 1/other.Z))/self.Z)
                child.UI = child.UI.subs(self.II,(self.II+other.II)* (1/(1/self.Z + 1/other.Z))/self.Z)
            children += self.TN 
            Zges = TN(1/(1/self.Z + 1/other.Z),self.UU,self.II+other.II,children)
            self.UU = Zges.UU 
            self.II = Zges.II * Zges.Z/self.Z
            self.UI = Zges.II * Zges.Z
            self.IU = Zges.UU / self.Z
            other.UU = Zges.UU 
            other.II = Zges.II * Zges.Z/other.Z
            other.UI = Zges.II * Zges.Z
            other.IU = Zges.UU / other.Z
            return Zges
class Netzwerk:
    def __init__(self,Us,Is,Zges):
        for child in Zges.TN:
            child.UU = child.UU.subs(Zges.UU,Us)
            child.IU = child.IU.subs(Zges.UU,Us)
            child.II = child.II.subs(Zges.II,Is)
            child.UI = child.UI.subs(Zges.II,Is)
        self.Z = simplify(factor(Zges.Z))
        self.TN = Zges.TN
        self.UU = simplify(factor(Zges.UU.subs(Zges.UU,Us)))
        self.II = simplify(factor(Zges.II.subs(Zges.II,Is)))
        self.UI = simplify(factor(Zges.UI.subs(Zges.II,Is)))
        self.IU = simplify(factor(Zges.IU.subs(Zges.UU,Us)))
class R(Z):
    def __init__(self,name):
        self.Z = Symbol(name)
        self.UU = Symbol('U_['+name+']')
        self.II = Symbol('I_['+name+']')
        self.UI = self.II * self.Z
        self.IU = self.UU / self.Z
        self.name = name
class L(Z):
    def __init__(self,name):
        self.Z = s*Symbol(name)
        self.UU = Symbol('U_['+name+']')
        self.II = Symbol('I_['+name+']')
        self.UI = self.II * self.Z
        self.IU = self.UU / self.Z
        self.name = name
class C(Z):
    def __init__(self,name):
        self.Z = 1/(s*Symbol(name))
        self.UU = Symbol('U_['+name+']')
        self.II = Symbol('I_['+name+']')
        self.UI = self.II * self.Z
        self.IU = self.UU / self.Z
        self.name = name

#Netzwerk Impedanzen definieren:
ZLh = L('Lh') # ZLx -> s*Lx
ZCh = C('Ch') # ZCx -> 1/(s*Cx)
ZRs = R('Rs') # ZR  -> R
ZRs2 = R('Rs2') # ZR  -> R
ZRr = R('Rr') # ZR  -> R

#Netzwerk Spannung & Strom definieren
Us, Is = symbols('Us Is')

#Netzwerk aufstellen
Nges = Netzwerk(Us,Is,(ZRs|ZCh+ZRr)|(ZLh|ZRr))

#Berechnete Variablen abrufen:
print('Zges = ' + str(Nges.Z))
print('ILh(Is) = ' + str(ZLh.I(Is)))
print('ILh(Us) = ' + str(ZLh.I(Us)))
