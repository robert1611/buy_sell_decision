from quandl_api import get_home_value_by_zip_code
from sql import get_rent_by_zip_code


def mortgage_calculation(zip_code, credit_score, has_been_bankrupt):

  credit_score = int(credit_score)
  has_been_bankrupt = int(has_been_bankrupt)

  house_purchase_value = get_home_value_by_zip_code(zip_code,4)
  house_rent_value_per_month = get_rent_by_zip_code(zip_code,4) 

  if has_been_bankrupt == 1 or credit_score < 500:
    return {
      'success': False,
      'message': 'Cannot give mortgage'
    }
  else:
    mortgage_percent = 0
    if credit_score > 740:
      mortgage_percent = 0.03
    elif credit_score > 600:
      mortgage_percent = 0.045
    else:
      mortgage_percent = 0.06

    mortgage_interest = mortgage_percent * house_purchase_value
    amortized_transaction_cost = (0.1 / 8) * house_purchase_value  #this can be an input on the front-end, but can be a default value
    repairs_cost = 0.01 * house_purchase_value
    insurance_cost = .008 * house_purchase_value
    property_tax = .0182 * house_purchase_value
    house_purchase_cost_per_month = (mortgage_interest + repairs_cost + insurance_cost + property_tax + amortized_transaction_cost) / 12

    option_result = 'RENT'
    if house_purchase_cost_per_month < house_rent_value_per_month:
      option_result = 'BUY'
    
    return {
      'success': True,
      'data': {
        'house_purchase_value': house_purchase_value,
        'mortgage_percent': mortgage_percent,
        'property_tax' : property_tax,
        'repairs_cost': repairs_cost,
        'insurance_cost' : insurance_cost,
        'mortgage_interest': mortgage_interest,
        'house_purchase_cost_per_month': house_purchase_cost_per_month,
        'amortized_transaction_cost' : amortized_transaction_cost,
        'house_rent_value_per_month': house_rent_value_per_month,
        'option_result': option_result
      }
    }
    