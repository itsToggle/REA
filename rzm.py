from sympy import * #Poly, degree, fraction, symbols, simplify, factor, mathematica_code, solve, solveset, Eq, sqrt
from sympy.parsing.sympy_parser import parse_expr
import copy

#Funktionen

#Important
s = Symbol('s')
Ti, Vr, Ta, Va, Tn, Vn, Tu, Vu, Te, Ve, Tin, Vrn, Tp= symbols('Ti Vr Ta Va Tn Vn Tu Vu Te Ve Tin Vrn Tp')

#<---Programm--->"
def Strang_Größen(Is_soll):
    print("<---Strang Größen--->")
    #Stranggrößen aus Raumzeiger:
    Is, Is1, Is2, Is3 = symbols('Is Is1 Is2 Is3')
    a = exp(I*2*pi/3)
    Is = 2/3*(Is1 + a*Is2 + a**2 * Is3)
    Is = nsimplify(Is,rational=True)
    print("Xs = " + str(mathematica_code(Is)))
    Is_soll = nsimplify(Is_soll,rational=True)
    Is1 = nsimplify(re(Is_soll),rational=True)
    Is2 = nsimplify(-1/2*re(Is_soll)+sqrt(3)/2*im(Is_soll),rational=True)
    Is3 = nsimplify(-1/2*re(Is_soll)-sqrt(3)/2*im(Is_soll),rational=True)
    print("Xs1 = " + str(mathematica_code(Is1)))
    print("Xs2 = " + str(mathematica_code(Is2)))
    print("Xs3 = " + str(mathematica_code(Is3)))
    print("")
    return Is1, Is2, Is3

def Clark(U1,U2,U3,leistungsinvariant=False,skalierung=True):
    print("<---Clark Travo--->")
    U_123 = Transpose(Matrix([[U1,U2,U3]]))
    T_Clark = Matrix([[1,-1/2,-1/2],[0,sqrt(3)/2,-sqrt(3)/2],[1/2, 1/2, 1/2]])
    if leistungsinvariant == True:
        F_Clark = sqrt(2/3)
    elif skalierung == True:
        F_Clark = 2/3
    else:
        F_Clark = 1
    U_ab0 = F_Clark * T_Clark * U_123
    Ua, Ub, U0 = U_ab0
    Ua = nsimplify(Ua,rational=True)
    Ub = nsimplify(Ub,rational=True)
    U0 = nsimplify(U0,rational=True)
    print("Xa = " + str(mathematica_code(Ua)))
    print("Xb = " + str(mathematica_code(Ub)))
    print("X0 = " + str(mathematica_code(U0)))
    print("")
    return Ua, Ub, U0

def Park(Ua, Ub, U0, theta=symbols('theta')):
    print("<---Park Travo--->")
    U_ab0 = Transpose(Matrix([[Ua,Ub,U0]]))
    T_Park = Matrix([[cos(theta),sin(theta),0],[-sin(theta),cos(theta),0],[0,0,1]])
    U_dq0 = T_Park * U_ab0
    Ud, Uq, U0 = U_dq0
    Ud = nsimplify(Ud,rational=True)
    Uq = nsimplify(Uq,rational=True)
    U0 = nsimplify(U0,rational=True)
    print("Xd = " + str(mathematica_code(Ud)))
    print("Xq = " + str(mathematica_code(Uq)))
    print("X0 = " + str(mathematica_code(U0)))
    print("")
    return Ud, Uq, U0



Us = 1+I*3

Us1, Us2, Us3 = Strang_Größen(Us)

Ua, Ub, U0 = Clark(Us1,Us2,Us3)

Ud, Uq, U0 = Park(Ua, Ub, U0)
