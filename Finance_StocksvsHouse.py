import matplotlib.pyplot as plt

years = [i for i in range(21, 62)]
total_housing_list = []
total_stock_list = []

j = 0
while j < len(years):

    #percentages
    av_house_appreciation_percentage = 6.5 #% bullish estimate
    av_inflation = 2.5 #%
    av_maintenance_property_tax_percentage = 2.5 #from overall house value
    av_SP_return_percentage = 10 #%
    av_mortgage_interest_percentage = 5 #% https://themortgagereports.com/61853/30-year-mortgage-rates-chart includes inflation
    av_rent_percentage_from_house_valuation = 1 #$ roughly 1% of house value

    #values
    init_investment = 100000 #$
    house_price = 500000 #$
    num_of_months_to_repay_house_loan = 240
    av_mortgage_monthly_interest_percentage = (av_mortgage_interest_percentage / 12) / 100 #12 months, percentage to decimal
    principal_house_loan_amt = house_price - init_investment
    num_yrs_mortgage = 20

    num_yrs_investment_fixed = years[j] #used for loop for rent profit
    num_yrs_investment_fixed2 = years[j] #used for loop for money not used in mortgage payments
    num_yrs_investment_fixed3 = years[j] #used for loop for money being added to stock market
    num_yrs_investment = years[j]
    j += 1
    '''
    The logic here is that the overall end housing amount is:
    extra money not being used for mortgage (including inflation - 20 to 40yrs) + rent profit (including inflation - 20 to 40yrs) + final house valuation (including inflation, 500k initial - 0 to 40yrs) - maintenance & property tax - mortgage payments (100k + monthly)

    M = P.r(1 + r)n/(1 + r)n - 1, where:
    M: Total monthly mortgage payment
    P: Principal loan amount
    r: Monthly interest rate
    n: Number of months required to repay the loan 

    FV = PV * (1+r)^n
    Where:
    FV is the future value of the house.
    PV is the present value or initial value of the house.
    r is the annual appreciation rate (expressed as a decimal, so 5% becomes 0.05).
    n is the number of years.
    '''

    #total mortgage paid (100k + monthly over 20 years)
    monthly_mortgage_payment = ((principal_house_loan_amt * av_mortgage_monthly_interest_percentage) * ((1 + av_mortgage_monthly_interest_percentage) ** num_of_months_to_repay_house_loan)) \
                                /(((1 + av_mortgage_monthly_interest_percentage) ** num_of_months_to_repay_house_loan) - 1)
    total_mortgage_paid_20yrs = (monthly_mortgage_payment * 12 * num_yrs_mortgage) + init_investment #12 months, 20 years of mortgage + initial investment

    #final house valuation (including inflation, 500k initial - 0 to 40yrs)
    final_house_valuation = house_price * (1 + (av_house_appreciation_percentage/100)) ** num_yrs_investment

    #find the total amount spent on maintenance and property tax
    total_maintenance_tax_cost = 0
    for year in range(1, num_yrs_investment + 1):
        house_price *= (1 + av_house_appreciation_percentage/100)
        annual_maintenance_propertytax_cost = house_price * (av_maintenance_property_tax_percentage/100) #roughly 2.5% of the house cost every year in maintenance and property tax
        total_maintenance_tax_cost += annual_maintenance_propertytax_cost

    #find the rent profit (including inflation - 20 to 40yrs)
    total_rent_profit = 0
    house_price = 500000
    num_yrs_investment = 0
    while num_yrs_investment < num_yrs_investment_fixed + 1:
        num_yrs_investment += 1
        house_price *= (1 + av_house_appreciation_percentage/100)
        if num_yrs_investment > num_yrs_mortgage:
            yearly_rent_profit = house_price * (av_rent_percentage_from_house_valuation/100) #roughly 1% rent
            total_rent_profit += (yearly_rent_profit * 12)

    #find extra money not being used for mortgage (including inflation - 20 to 40yrs)
    total_money_not_used_mortgage_including_inflation = 0
    num_yrs_investment = 0
    yearly_mortgage_payment = monthly_mortgage_payment * 12
    while num_yrs_investment < num_yrs_investment_fixed2 + 1:
        num_yrs_investment += 1
        yearly_mortgage_payment *= (1 + (av_inflation/100))
        if num_yrs_investment <= num_yrs_mortgage:
            total_money_not_used_mortgage_including_inflation += yearly_mortgage_payment - (12 * monthly_mortgage_payment)
        if num_yrs_investment > num_yrs_mortgage:
            total_money_not_used_mortgage_including_inflation += yearly_mortgage_payment
        total_money_not_used_mortgage_including_inflation *= (1 + (av_SP_return_percentage/100))

    total_housing_investment = total_money_not_used_mortgage_including_inflation + total_rent_profit + final_house_valuation - total_maintenance_tax_cost - total_mortgage_paid_20yrs
    total_housing_list.append(total_housing_investment)

    print(total_money_not_used_mortgage_including_inflation)
    print(total_rent_profit)
    print(final_house_valuation)
    print(total_maintenance_tax_cost)
    print(total_mortgage_paid_20yrs)
    print(total_housing_investment)

    '''
    For the stock market its a compount interest formula with:

    100k as the initial investment
    the mortage monthly payment added to the stock market every month with the caveat being that this amount is also undergoing inflation
    Using the S&P 500 return rate
    '''

    #find extra money not being used for mortgage (including inflation - 20 to 40yrs)
    total_money_in_stock = 100000 #based on initial investment
    num_yrs_investment = 0
    yearly_mortgage_payment = monthly_mortgage_payment * 12
    while num_yrs_investment < num_yrs_investment_fixed3 + 1:
        num_yrs_investment += 1
        yearly_mortgage_payment *= (1 + (av_inflation/100))
        total_money_in_stock += yearly_mortgage_payment
        total_money_in_stock *= (1 + (av_SP_return_percentage/100))

    total_stock_list.append(total_money_in_stock)
    print(total_money_in_stock)

plt.figure(figsize=(12, 6))
# First subplot: Total Money in Stock vs. Total Housing Investment
plt.subplot(211)
plt.plot(years, total_stock_list, label='Total Money in Stock')
plt.plot(years, total_housing_list, label='Total Housing Investment')
plt.xlabel('Years')
plt.ylabel('Total Value')
plt.title('Total Money in Stock vs. Total Housing Investment')
plt.legend()
# Calculate the ratio of money in stock to housing investment for each year
ratio_list = [stock / housing for stock, housing in zip(total_stock_list, total_housing_list)]
plt.subplot(212)
plt.plot(years, ratio_list, label='Money in Stock to Housing Investment Ratio', color='green')
plt.xlabel('Years')
plt.ylabel('Ratio')
plt.title('Ratio of Money in Stock to Housing Investment over Time')
plt.legend()
plt.tight_layout()
plt.show()