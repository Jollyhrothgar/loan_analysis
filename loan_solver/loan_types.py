# TODO abstract with factory once many loan types are needed
class StudentLoan(object):
    def __init__(self, name, rate, ltype, interest, principal):
        self.name = name
        self.rate = rate
        self.ltype = ltype
        self.interest = interest
        self.principal = principal
        
    def __repr__(self):
        return 'Loan Name: {}, Principal: {}, Unpaid Interest: {}, Interest Rate: {}, Loan Type: {}'.format(self.name, self.principal, self.interest, self.rate, self.ltype)
    
    def copy(self):
        return StudentLoan(self.name, self.rate, self.ltype, self.interest, self.principal)
     
