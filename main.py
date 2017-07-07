import requests

# API URIs

base_url = "https://api.infojobs.net/api/1"
get_job_offers = "/offer"
get_provinces = "/dictionary/province"
get_categories = "/dictionary/category"
get_subcategories = "/dictionary/subcategory"
get_cities= "/dictionary/city"


# Authentication

client_id = "ab7ac04688174782a8269c5adc7bde6c"
client_secret = "Gnt7Tqgb4fUctqOMKXWjJg9YPGKKPP+PDgd6r/B0tdsjPEqbmp"

# Parameters

keywords = ''
province = 'Ourense'
city = 'Ourense'
payload = {'q': keywords, 'province': province}

#publishedMax




# Main query

url = base_url + get_job_offers
myResponse = requests.get(url, auth=(client_id, client_secret), params=payload)


print (myResponse.content)

