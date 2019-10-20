
def integration_y_by_c_of_y (b_a, lambda_, b):
    int_ = (b_a**2/2) + (2*(lambda_ - 1)*b_a**3)/(b*3)
    print("!")
    return int_
def control_derivative (tau_, c_lalpha, Sref, b, lambda_, CR, b1, b2 ):
    print("!!")
    Cldela = (2*tau_*c_lalpha/(Sref*b))*CR*(integration_y_by_c_of_y(b1, lambda_, b) \
                                            - integration_y_by_c_of_y(b2, lambda_, b))
    return Cldela
tau_ = 0.47

c_lalpha = 0.115

Sref = 93.5

b = 28.08

lambda_ = 0.235

CR = 5.39

b1 = 14.04

b2 = 9.126

C = control_derivative(tau_, c_lalpha, Sref, b, lambda_, CR, b1, b2 )
print(C)

