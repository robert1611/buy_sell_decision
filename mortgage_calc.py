#from quandl_api import get_home_value_by_zip_code
from sql import get_rent_by_zip_code, DecisionMaker, session, get_value_by_zip_code


def mortgage_calculation(zip_code, credit_score, has_been_bankrupt, years_to_live):

  credit_score = int(credit_score)
  has_been_bankrupt = int(has_been_bankrupt)
  years_to_live = int(years_to_live)

  house_purchase_value = get_value_by_zip_code(zip_code)
  house_rent_value_per_month = get_rent_by_zip_code(zip_code)
  



  if has_been_bankrupt == 1 or credit_score < 500:
    return {
      'success': False,
      'message': 'Cannot give mortgage'
    }
  else:
    mortgage_percent = 0
    if credit_score > 740:
      mortgage_percent = 0.0275
    elif credit_score > 600:
      mortgage_percent = 0.045
    else:
      mortgage_percent = 0.06

    mortgage_interest = round(mortgage_percent * house_purchase_value)
    amortized_transaction_cost = round((0.1 / years_to_live) * house_purchase_value) #this can be an input on the front-end, but can be a default value
    repairs_cost = round(0.01 * house_purchase_value)
    insurance_cost = round(.008 * house_purchase_value)
    property_tax = round(.0182 * house_purchase_value)
    house_purchase_cost_per_month = round(mortgage_interest + repairs_cost + insurance_cost + property_tax + amortized_transaction_cost) / 12
    house_purchase_cost_per_month = round(house_purchase_cost_per_month)


    option_result = 'RENT'
    if house_purchase_cost_per_month < house_rent_value_per_month:
      option_result = 'BUY'
    
    result = {
        'house_purchase_value': house_purchase_value,
        'mortgage_percent': mortgage_percent,
        'property_tax' : property_tax,
        'repairs_cost': repairs_cost,
        'insurance_cost' : insurance_cost,
        'mortgage_interest': mortgage_interest,
        'house_purchase_cost_per_month': house_purchase_cost_per_month,
        'amortized_transaction_cost' : amortized_transaction_cost,
        'house_rent_value_per_month': house_rent_value_per_month,
        'option_result': option_result,
        'credit_score' : credit_score,
        'zip_code' : zip_code,
        'years_to_live' : years_to_live,
        'has_been_bankrupt' : has_been_bankrupt,

      }
    decision_maker = DecisionMaker(**result)
    session.add(decision_maker)
    session.commit()

    return {
      'success': True,
      'data': result 
        
    }
    