# Student Loan Explorer

The goal of this repo is to provide tools to folks to understand how their student loan repayment plan will proceed. A few different scenarios are provided in the jupyter notebook representing different payment strategies.

The overall goal of this repo is to provide users with a payment strategy which they can follow with minmal effort that minimizes the amount of interest they pay to student loan lenders.

Often times, one gets simplistic advice such as "do the snowball method" or "do the avalanche method". This is fine, but what if a different strategy could reduce either your loan payoff time, or the total interest you pay? 

While the single biggest factor in reducing the payoff time and paid interest is obviously the size of your monthly payment, there are secondary factors which might affect how you allocate payments. This is because generally, the ONLY parameter people can control with regards to student loans is how much they pay - nothing else.

This tool opts to additionally provide some means to answer common questions like:

- If I have N loans with X interest rates, how much do I have to pay if I want to pay off these loans in 5 years?
- How should I allocate my monthly payment if I have more than one loan?
- Will I save more money if I pay down one large loan while allowing smaller loans to accumulate interest?

I hope to address all these questions and more.

# TODO

- Double check the pay\_loan method, I think something is wonky.
- Add different kinds of debt, such as credit-card payments and car payments
- Make more user-friendly. Goal is basically a website that a non-expert can use, potentially via exposed jupyter notebook widgets.
- Fix package import for loan\_solver, gotta remind myself of how this works.
