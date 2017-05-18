from loan_types import *
class LoanSolver(object):
    ''' Loans are added and stored as dictionaries in self.loans list. 
    Current and initial loan state is tracked.'''
    
    def __init__(self):
        self.loans = {}
        # Stores all loans which have been paid off at their initial state.
        self.paid_loans = {}
        self.total_paid = 0
        
        # Convert time into years by supplying the appropriate unit
        self._allowed_time_units = {
            'hour':lambda x:x/8760.,
            'day':lambda x:x/365.,
            'minute':lambda x:x/525600.,
            'second':lambda x:x/31536000.,
            'year':lambda x:x,
            'month':lambda x:x/12.,
        }
        
        # Factory methods for supported loan types - different 
        # loans may have different attributes, so each loan 
        # type gets its own generator.
        self._loan_types = {
            'StudentLoan':StudentLoan
        }
        
        
    def add_loan(self, loan_name, loan_type, interest_rate, principal_balance, interest_balance=0.):
        '''Adds a loan to the loan set. Interest rate is assumed to be APR 
        
        :param: loan_name (str) - The name for the loan, must be unique
        :param: loan_type (str) - The type of loan, defines the rules for
            interest recapitalization and other specific loan information
        :param: interest_rate (float) - yearly fractional interest rate 
            (ex 0.5 = 50%) for a whole year
           
        Math assumes time to be in years, therefore all times are 
        expressed internally as fractions of years so as to use the familiar
        compounding interest formula:
        
            F(t) = Principal * exp( rate * time_in_years ) 
            
        '''
        # generate new instance of StudentLoan (add more loan types as needed)
        if loan_type not in self._loan_types:
            raise ValueError('Loan type {} is not yet supported. Available types are {}'.format(loan_type, repr(self._loan_types.keys())))
        if loan_name in self.loans:
            raise ValueError('Loan with name {} already exists'.format(loan_name))
        loan = self._loan_types[loan_type](
            name=loan_name, 
            rate=interest_rate, 
            ltype=loan_type,
            principal=principal_balance,
            interest=interest_balance,
        )
        self.loans[loan_name]=loan
        self.paid_loans[loan_name] = loan.copy()
    
    def get_initial_principal(self):
        ''' gets the initial principal'''
        return sum([l.principal for l in self.paid_loans.values()])
    
    def get_initial_interest(self):
        return sum([l.interest for l in self.paid_loans.values()])
    
    def get_initial_debt(self):
        return self.get_initial_principal() + self.get_initial_interest()
    
    def recapitalize(self, loan_type=None, loan_name=None):
        '''Recapitalizes the interest in all loans in self.loans. If 
        loan_name is specified, all loans mathing the name will be 
        recapitalized. If loan_type is specified, all loans matching 
        that type will be recapitalized. If loan_name and loan_type 
        are specified, only loans matching the name and type will be 
        recapitalized.
        
        :param: loan_name (str) recapitalize only loans matching this name
        :param: loan_type (str) recapitalize only loans matching this name
        
        Since loan_name is already enough to uniquely identify a loan, 
        the loan_type is ignored in cases where loan_type is specified.
        
        If loan_name, loan_type are not set, then all loans 
        will be recapitalized.
        '''
        
        for loan in self.loans.values():
            if loan_type is not None and loan_name is None:
                if loan_type == loan.ltype:
                    loan.principal += loan.interest
                    loan.interest = 0
            if loan_name is not None:
                if loan_name == loan.name:
                    loan.principal += loan.interest
                    loan.interest = 0
            else:
                loan.principal += loan.interest
                loan.interest = 0
                
    def add_interest(self, amount_of_time, time_unit='years'):
        unit = time_unit.lower()
        if unit not in self._allowed_time_units:
            raise ValueError("Allowed time units are: {}".repr(self._allowed_time_units.keys()))
        delta_t = self._allowed_time_units[unit](amount_of_time)
        
        for loan in self.loans.values():
            loan.interest = loan.principal * np.exp(loan.rate * delta_t) - loan.principal
    
    def debt_free(self):
        if not self.loans:
            return True
        else:
            return False
        
    # TODO handle remainder better - this must be done outside the class to maintain flexibility
    def pay_loan(self, loan_name, payment, excess='largest_interest'):
        ''' pay amount to loan_name. Payment applies first to interest, and then to principal
        Returns either 0 or unspent money'''
        excess_name = {
            'largest_interest':self.largest_interest_rate,
            'lowest_interest':self.smallest_interest_rate,
            'largest_principal':self.largest_principal,
            'lowest_principal':self.smallest_principal,
        }
        
        if loan_name not in self.loans:
            return payment
    
        if excess not in excess_name: 
            raise ValueError("You can apply excees payment to {} but you specified {}".format(repr(excess_name.keys()), excess))
        
        # if all debts are paid, then we can't apply a payment anywhere.
        if self.debt_free():
            return payment
        self.total_paid += payment
        if payment <= self.loans[loan_name].interest:
            self.loans[loan_name].interest = self.loans[loan_name].interest - payment
            return 0.
        else:
            payment = payment - self.loans[loan_name].interest
            self.loans[loan_name].interest = 0.
            # apply remaining payment to principal
        if payment < self.loans[loan_name].principal:
            self.loans[loan_name].principal = self.loans[loan_name].principal - payment
            return 0 
        elif payment >= self.loans[loan_name].principal:
            payment -= self.loans[loan_name].principal
            self.loans[loan_name].principal = 0.
            del self.loans[loan_name]
            self.total_paid - payment # overcounted.
            
            # Since most people will just use all the payment.
            loan_name = excess_name[excess]()
            if loan_name is None:
                return payment
            if self.debt_free():
                return payment
            return self.pay_loan(loan_name, payment, excess)
        
    def print_loan_state(self):
        for loan in self.loans.values():
            print(loan)
            
    def get_total_debt(self):
        '''returns dict of total_debt, total_interest '''
        total_principal = sum([loan.principal for loan in self.loans.values()])
        total_interest = sum([loan.interest for loan in self.loans.values()])
        debt = {'principal':total_principal, 'interest':total_interest}
        return debt
    
    def get_balance_distribution(self):
        ''' returns each loan's fraction of the total debt '''
        debt = self.get_total_debt()
        summed_debt = sum([val for val in debt.values()])
        distribution = {loan.name:(loan.principal + loan.interest)/summed_debt for loan in self.loans.values() }
        return distribution
    
    def get_interest_distribution(self):
        ''' return each loan's fraction of the total interest rate '''
        total_interest = sum([loan.rate for loan in self.loans.values()])
        distribution = {loan.name:(loan.rate/total_interest) for loan in self.loans.values() }
        return distribution
    
    def largest_interest_rate(self):
        try:
            return sorted(self.loans.items(), key=lambda x:x[1].interest)[-1][1].name
        except:
            return None
    
    def smallest_interest_rate(self):
        try:
            return sorted(self.loans.items(), key=lambda x:x[1].interest)[0][1].name
        except:
            return None
    
    def largest_principal(self):
        try:
            return sorted(self.loans.items(), key=lambda x:x[1].principal)[-1][1].name
        except:
            return None
    
    def smallest_principal(self):
        try:
            return sorted(self.loans.items(), key=lambda x:x[1].principal)[0][1].name
        except:
            return None
