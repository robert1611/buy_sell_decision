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

    mortgage_cost = mortgage_percent * house_purchase_value
    transaction_cost = (0.00001 / 8) * house_purchase_value
    repairs_cost = 0.01 * house_purchase_value
    insurance_cost = .008 * house_purchase_value
    property_tax = .02 * house_purchase_value
    house_purchase_cost_per_month = (mortgage_cost + repairs_cost + insurance_cost + property_tax + transaction_cost) / 12

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
        'mortgage_cost': mortgage_cost,
        'house_purchase_cost_per_month': house_purchase_cost_per_month,
        'house_rent_value_per_month': house_rent_value_per_month,
        'option_result': option_result
      }
    }
    