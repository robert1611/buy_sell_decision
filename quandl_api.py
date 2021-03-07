import quandl
from os import quandl

API_KEY = environ['QUANDL_API_KEY']
quandl.ApiConfig.api_key = API_KEY

def get_home_value_by_zip_code(zip_code, no_of_bedrooms):
  indicator_id = "ZSFH"
  if no_of_bedrooms == 2:
    indicator_id = "ZSFH"
  data = quandl.get_table("ZILLOW/DATA", indicator_id=indicator_id, region_id=zip_code)
  return data.iloc[0].value
