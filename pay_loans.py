from loan_calc import LoanManager
loans = [
    {
        # Minimum Payment
        'loan_name':'loan_641',
        'loan_type':'StudentLoan',
        'principal_balance':6507.64,
        'interest_rate':0.0641
    },
    {
        # Minimum Payment
        'loan_name':'loan_541',
        'loan_type':'StudentLoan',
        'principal_balance':21263.06,
        'interest_rate':0.0541,
    },
    {
        # Minimum Payment
        'loan_name':'loan_790',
        'loan_type':'StudentLoan',
        'principal_balance':6994.65,
        'interest_rate':0.068,
    },
    {
        # Minimum Payment
        'loan_name':'loan_680',
        'loan_type':'StudentLoan',
        'principal_balance':23562.73,
        'interest_rate':0.068,
    },
]

def always_pay_highest_balance(payment, time_unit='month', loans=loans):
    print("Calculating Pay According to Balance - Payment is split according to balance distribution")
    solver = LoanManager()
    for loan in loans:
        solver.add_loan(**loan)
    done = False
    time = 0
    # Pay According To Loan Amount
    while not done:
        solver.add_interest(1,time_unit)
        time += 1
        distribution = solver.get_balance_distribution()
        # TODO - fix how remainder is applied, if any (returns from pay_loan)
        for loan_name in distribution:
            solver.pay_loan(loan_name, payment*distribution[loan_name], excess_rule='largest_balance')
            solver.check_payments()
        if solver.debt_free():
            done = True
            print("\tTotal Paid {}, Principal {}, Total Interest {}, in {} {}s, {} {}s".format(solver.get_total_paid(), solver.get_initial_balance(), solver.get_interest_paid(), time, time_unit, time/12., "year"))

def always_pay_highest_interest(payment, time_unit='month', loans=loans):
    # Pay According to Interest Amount
    print("Calculating Pay According to Interest - Payment is split according to the interest distribution")
    solver = LoanManager()
    for loan in loans:
        solver.add_loan(**loan)
    time = 0
    done = False
    while not done:
        solver.add_interest(1,time_unit)
        distribution = solver.get_interest_distribution()
        time += 1
        for loan_name in distribution:
            solver.pay_loan(loan_name, payment*distribution[loan_name], excess_rule='largest_interest_rate')
        if solver.debt_free():
            done = True
            print("\tTotal Paid {}, Principal {}, Total Interest {}, in {} {}s, {} {}s".format(solver.get_total_paid(), solver.get_initial_balance(), solver.get_interest_paid(), time, time_unit, time/12., "year"))

def pay_snowball(payment, time_unit='month', loans=loans):
    # Snowball
    print("Calculating Snowball Method")
    solver = LoanManager()
    for loan in loans:
        solver.add_loan(**loan)
    time = 0
    done = False
    loan_name = solver.smallest_balance()
    while not done:
        solver.add_interest(1,time_unit)
        time += 1
        solver.pay_loan(loan_name, payment, excess_rule='smallest_balance')
        if loan_name not in solver.loans:
            # a loan is paid off
            loan_name = solver.smallest_balance()
            if loan_name is None:
                done = True
                print("\tTotal Paid {}, Principal {}, Total Interest {}, in {} {}s, {} {}s".format(solver.get_total_paid(), solver.get_initial_balance(), solver.get_interest_paid(), time, time_unit, time/12., "year"))
        
def pay_avalanche(payment, time_unit='month', loans=loans):
    # Avalanche
    # TODO - pick the largest loan and pay off entirely, not continuously the largest balance
    print("Calculating Avalanche Method")
    solver = LoanManager()
    for loan in loans:
        solver.add_loan(**loan)
    time = 0
    done = False
    loan_name = solver.largest_balance()
    while not done:
        solver.add_interest(1,time_unit)
        time += 1
        solver.pay_loan(loan_name, payment, excess_rule='largest_balance')
        if loan_name not in solver.loans:
            # a loan is paid off
            loan_name = solver.largest_balance()
            if loan_name is None:
                done = True
                print("\tTotal Paid {}, Principal {}, Total Interest {}, in {} {}s, {} {}s".format(solver.get_total_paid(), solver.get_initial_balance(), solver.get_interest_paid(), time, time_unit, time/12., "year"))

def pay_highest_potential_interest(payment, time_unit='month', loans=loans):
    print("Calculating 'highest potential interest' method")
    solver = LoanManager()
    for loan in loans:
        solver.add_loan(**loan)
    time = 0
    done = False
    while not done:
        solver.add_interest(1, time_unit)
        time += 1
        loans = [(loan_name, loan.principal*loan.rate) for loan_name,loan in solver.loans.items()]
        loans = sorted(loans, key=lambda x:x[1], reverse=True)
        loan_name = loans[0][0]

        solver.pay_loan(loan_name, payment, excess_rule='largest_interest_rate')

        if solver.debt_free():
            done = True
            print("\tTotal Paid {}, Principal {}, Total Interest {}, in {} {}s, {} {}s".format(solver.get_total_paid(), solver.get_initial_balance(), solver.get_interest_paid(), time, time_unit, time/12., "year"))

if __name__ == '__main__':
    payment = 2000
    always_pay_highest_balance(payment)
    always_pay_highest_interest(payment)
    pay_snowball(payment)
    pay_avalanche(payment)
    pay_highest_potential_interest(payment)
