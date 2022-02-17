from sympy import * #Poly, degree, fraction, symbols, simplify, factor, mathematica_code, solve, solveset, Eq, sqrt
from sympy.parsing.sympy_parser import parse_expr
import copy

#Glieder
class PI:
    def __new__(cls,Vr,Ti,mode='Vr'):
        if mode == 'Vr':
            string = (Vr)*((Ti)*s+1)/((Ti)*s)
        else:
            string = (Vr)*(((Vr)/(Ti))*s+1)/(((Vr)/(Ti))*s)
        return string
class PT1:
    def __new__(cls,Va,Ta):
        string = (Va)/((Ta)*s+1)
        return string
class I:
    def __new__(cls,Tn):
        string = 1/((Tn)*s)
        return string
class P:
    def __new__(cls,Vr):
        string = (Vr)
        return string
class PTD:
    def __new__(cls,Vr,Td,Tr):
        string = (Vr)*(((Td)*s+1)/((Tr)*s+1))
        return string
#Funktionen
def kompensiert(Gk,Zeitkonstanten,Ersatz=[]):
    print("Pole/Nsten werden kompensiert:")
    n,d = fraction(Gk)
    Nsts = solve(Poly(n,s),s)
    n = degree(Poly(n,s))
    d = degree(Poly(d,s))
    print("Gk(s) = " + str(mathematica_code(Gk)))
    print("Zähler Ordnung: " + str(n) + " / Nenner Ordnung: " + str(d))
    komp_count = 0
    Kompensationen = []
    neueZeitkonstanten = copy.deepcopy(Zeitkonstanten)
    for Zeitkonstante in Zeitkonstanten:
        for Nst in Nsts:
            if not str(Nst) == '0':
                Nst = -1/Nst
                if not str(Nst) in str(Zeitkonstanten) and not str(Nst) in str(Ersatz):
                    GkTest = Gk.subs(Zeitkonstante,Nst)
                    GkTest = simplify(factor(GkTest))
                    nTest,dTest = fraction(GkTest)
                    nTest = degree(Poly(nTest,s))
                    dTest = degree(Poly(dTest,s))
                    if (nTest < n or dTest < d):
                        Kompensationen += [[Zeitkonstante, Nst]]
                        print("Nst kompensiert: " + str(Zeitkonstante) + " -> " + str(Nst))              
    for Kompensation in Kompensationen:
        komp_count += 1
        Gk = Gk.subs(Kompensation[0],Kompensation[1])
        for Zeitkonstante in neueZeitkonstanten:
            if Zeitkonstante == Kompensation[0]:
                Zeitkonstante = Kompensation[1]
    n,d = fraction(Gk)
    Pols = solve(Poly(d,s),s)
    n = degree(Poly(n,s))
    d = degree(Poly(d,s))
    Kompensationen = []
    for Zeitkonstante in Zeitkonstanten:
        for Pol in Pols:
            if not str(Pol) == '0':
                Pol = -1/Pol
                if not str(Pol) in str(Zeitkonstanten) and not str(Pol) in str(Ersatz):
                    GkTest = Gk.subs(Zeitkonstante,Pol)
                    GkTest = simplify(factor(GkTest))
                    nTest,dTest = fraction(GkTest)
                    nTest = degree(Poly(nTest,s))
                    dTest = degree(Poly(dTest,s))
                    if (nTest < n or dTest < d):
                        Kompensationen += [[Zeitkonstante, Pol]]
                        print("Pol kompensiert: " + str(Zeitkonstante) + " -> " + str(Pol))
    for Kompensation in Kompensationen:
        komp_count += 1
        Gk = Gk.subs(Kompensation[0],Kompensation[1])
        for index,Zeitkonstante in enumerate(neueZeitkonstanten):
            if Zeitkonstante == Kompensation[0]:
                neueZeitkonstanten[index] = Kompensation[1]
    n,d = fraction(Gk)
    n = degree(Poly(n,s))
    d = degree(Poly(d,s))
    if not komp_count == 0:
        print("Gk(s) = " + str(mathematica_code(Gk)))
        print("Zähler Ordnung: " + str(n) + " / Nenner Ordnung: " + str(d))
    else:
        print("Es konnten keine Pole/Nsten kompensiert werden!")
    print("")
    return Gk, neueZeitkonstanten
def Gk_Gg(Gk):
    #Ausgabe offener Kreis, geschlossener Kreis
    Gg = Gk/(1+Gk)
    Gk = simplify(factor(Gk))
    Gg = simplify(factor(Gg))
    print("Übertragungsfunktionen: ")
    print("Gk(s) = " + str(mathematica_code(Gk)))
    print("Gg(s) = " + str(mathematica_code(Gg)))
    print("")
    return Gk, Gg
def normiertes_Polynom(Gg):
    print("Polynomform: ")
    n,d = fraction(Gg)
    n = Poly(n,s)
    d = Poly(d,s)
    degree_n = degree(n)
    degree_d = degree(d)
    n_coeff_dict = dict({s**m[0]:n.coeff_monomial(m) for m in n.monoms()})
    d_coeff_dict = dict({s**m[0]:d.coeff_monomial(m) for m in d.monoms()})
    if 1 in d_coeff_dict:
        for monom in n_coeff_dict:
            n_coeff_dict[monom] = n_coeff_dict[monom] / d_coeff_dict[1]
        for monom in d_coeff_dict:
            d_coeff_dict[monom] = d_coeff_dict[monom] / d_coeff_dict[1]
    n = []
    d = []
    for m in n_coeff_dict:
        n += [str(m) + " * " + str(n_coeff_dict[m])]
    for m in d_coeff_dict:
        d += [str(m) + " * " + str(d_coeff_dict[m])]
    n = " + ".join(n)
    d = " + ".join(d)
    n = parse_expr(n)
    d = parse_expr(d)
    Gg = n/d
    print("Gg(s) = " + str(mathematica_code(Gg)))
    print("Zähler Polynome ("+str(degree_n)+".Ordnung): " + str(mathematica_code(n_coeff_dict)))
    print("Nenner Polynome ("+str(degree_d)+".Ordnung): " + str(mathematica_code(d_coeff_dict)))
    print("")
    return Gg
def Dämpfungsform(Gg, Vr, D=symbols('D'), Q=symbols('Q')):
    n,d = fraction(Gg)
    n = Poly(n,s)
    d = Poly(d,s)
    n_coeff_dict = dict({s**m[0]:n.coeff_monomial(m) for m in n.monoms()})
    d_coeff_dict = dict({s**m[0]:d.coeff_monomial(m) for m in d.monoms()})
    if not s**3 in d_coeff_dict:
        #Ausgabe der Polynome des Nenners des Geschlossenen Kreises in Dämpfungsform 2.Ordnung
        print("Dämpfungsform 2ter Ordnung:")
        w0 = sqrt(1/d_coeff_dict[s**2])
        Vrnew = solveset(Eq(d_coeff_dict[s],2*D/w0),Vr)
        Vrnew = Vrnew.args[0]
        Gg = Gg.subs(Vr,Vrnew)
        print("w0 = " + str(w0))
        print("D = " + str(D))
        print("Vr = " + str(Vrnew))
        print("")
    else:
        #Ausgabe der Polynome des Nenners des Geschlossenen Kreises in Dämpfungsform 3.Ordnung
        print("Dämpfungsform 3ter Ordnung:")
        w0 = (Q+2*D)/d_coeff_dict[s]
        Vrnew = solveset(Eq(d_coeff_dict[s**3],Q/w0**3),Vr)
        Vrnew = Vrnew.args[0].args[0]
        Gg = Gg.subs(Vr,Vrnew)
        print("w0 = " + str(w0))
        print("D = " + str(D))
        print("Vr = " + str(Vrnew))
        print("")
    return Gg, Vrnew
def symmetrisches_Optimum(Gg, Vr, Ti, D=symbols('D')):
    n,d = fraction(Gg)
    n = Poly(n,s)
    d = Poly(d,s)
    a = 2*D+1
    Tinew = a**2 * Te
    Vrnew = 1/a * Tn/Te
    Gg = Gg.subs(Vr,Vrnew)
    Gg = Gg.subs(Ti,Tinew)
    print("a = " + str(a))
    print("Vr = " + str(Vrnew))
    print("Ti = " + str(Tinew))
    print("")
    return Gg, Vr, Ti
def zu_PT1_Ersatzglied(Gg,Vre):
    n,d = fraction(Gg)
    n = Poly(n,s)
    d = Poly(d,s)
    n_coeff_dict = dict({s**m[0]:n.coeff_monomial(m) for m in n.monoms()})
    d_coeff_dict = dict({s**m[0]:d.coeff_monomial(m) for m in d.monoms()})
    #Ausgabe der PT1 Parameter (Ersatzglied)
    print("Ersatzgrößen: ")
    if not s in n_coeff_dict:
        n_coeff_dict[s] = 0
    Ve = n_coeff_dict[1]/d_coeff_dict[1]
    Te = d_coeff_dict[s]/d_coeff_dict[1] - n_coeff_dict[s]/n_coeff_dict[1]
    print("Ve = " + str(Ve))
    print("Te = " + str(Te))
    print("")
    return Ve, Te

s, D, Q, w0, a = symbols('s D Q w0 a')
Ti, Vr, Ta, Va, Tn, Vn, Tu, Vu, Te, Ve, Tin, Vrn, Tp= symbols('Ti Vr Ta Va Tn Vn Tu Vu Te Ve Tin Vrn Tp')
Ra, La = symbols('Ra La')

# #Gleichstrom Maschine, Strom und Drehzahlregelung
# #Übung 3-4
# #Variablen:
# s, D, Q, w0, a = symbols('s D Q w0 a')
# Ti, Vr, Ta, Va, Tn, Vn, Tu, Vu, Te, Ve, Tin, Vrn, Tp= symbols('Ti Vr Ta Va Tn Vn Tu Vu Te Ve Tin Vrn Tp')
# Ra, La = symbols('Ra La')
# #Programm:
# print("<---Offene Strom Regelstrecke--->")
# Gk = PI(Vr,Ti) * PT1(1,Te) * PT1(1/Ra,La/Ra) #<------------------------------------------------------------Offener Kreis der Stromregelung
# Gk,[Ti] = kompensiert(Gk,[Ti],Ersatz=[Te])
# Gk, Gg = Gk_Gg(Gk)
# Gg = normiertes_Polynom(Gg)
# print("<---PI Auslegung: Stromregelung--->")
# Gg, Vr = Dämpfungsform(Gg,Vr,D=1/sqrt(2))
# Gg = normiertes_Polynom(Gg)
# print("<---Stromregelung zu PT1 Ersatzglied--->")
# Ve, Te = zu_PT1_Ersatzglied(Gg,Vr)
# print("<---Offene Drehzahl Regelstrecke--->")
# Gk = PI(Vrn,Tin) * PT1(Ve,Te) * I(Tn)   #<--------------------------------------------------------------Offener Kreis der Drehzahlregelung
# Gk = normiertes_Polynom(Gk)
# print("<---PI Auslegung: Drehzahlregelung--->")
# Gk, Vr, Ti = symmetrisches_Optimum(Gk,Vr,Ti,D=1)


#Gleichstrom Maschine, Lageregelung
#Übung 6
#Variablen:
s, D, Q, w0, a = symbols('s D Q w0 a')
Ti, Vr, Ta, Va, Tn, Vn, Tu, Vu, Te, Ve, Tin, Vrn, Tp= symbols('Ti Vr Ta Va Tn Vn Tu Vu Te Ve Tin Vrn Tp')
Ra, La = symbols('Ra La')
#Programm:
print("<---Innere Regelstrecke--->")
Gk = PI(1/a*Tn/Te,a**2*Te) * PT1(1,Te) * I(Tn)
Gk, Gg = Gk_Gg(Gk)
print("<---PT1-Regler--->")
Gke = PT1(Vr,Ti) * Gg * I(Tu)
Gke, [Ti]= kompensiert(Gke,[Ti])
Gke, Gge = Gk_Gg(Gke)
Gge = normiertes_Polynom(Gge)
print("<---PTD-Regler--->")
Gke = PTD(Vr,Ti,Tp) * Gg * I(Tu)
Gke, [Ti,Tp] = kompensiert(Gke,[Ti,Tp])
Gke, Gge = Gk_Gg(Gke)
Gge = normiertes_Polynom(Gge)
Gge, Vr = Dämpfungsform(Gge,Vr)
