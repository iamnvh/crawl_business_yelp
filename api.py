from googleplaces import GooglePlaces, types, lang, GooglePlacesError
import time, json
from decimal import *
from get_place import get_place

# You may prefer to use the text_search API, instead.
#[types.TYPE_CLOTHING_STORE] or [types.TYPE_CAFE] or [types.TYPE_GROCERY_OR_SUPERMARKET] or [types.TYPE_BEAUTY_SALON] or 
data_last = []
data_backup = []

def get_info_business_by_googleApi(api_key, location, type):
    if type == 'cafe':
        types = types.TYPE_CAFE
    if type == 'clothing':
        types = types.TYPE_CLOTHING_STORE
    if type == 'Grocery':
        types = types.TYPE_GROCERY_OR_SUPERMARKET
    if type == 'salon':
        types = types.TYPE_BEAUTY_SALON
    google_places = GooglePlaces(api_key)
    lat = location.split(',')[0]
    lng = location.split(',')[1]
    query_result = google_places.nearby_search(
        language=lang.ENGLISH,lat_lng={'lat': lat, 'lng': lng},radius=1000,types=[types]
    )
    if query_result.has_attributions:
        print(query_result.html_attributions)
    
    # Step 1
    step1, step1_backup = get_place(query_result, api_key)
    data_last.extend(step1)
    data_backup.extend(step1_backup)

    # Are there any additional pages of results?
    if query_result.has_next_page_token:
        query_result_next_page = google_places.nearby_search(
            pagetoken=query_result.next_page_token,lat_lng={'lat': lat, 'lng': lng},radius=1000, types=[types]
        )
        step2, step2_backup = get_place(query_result_next_page, api_key)
        data_last.extend(step2)
        data_backup.extend(step2_backup)
        
        if query_result_next_page.has_next_page_token:
            time.sleep(3)
            query_result_next_page_2 = google_places.nearby_search(
                pagetoken=query_result_next_page.next_page_token,lat_lng={'lat': lat, 'lng': lng},radius=1000, types=[types]
            )
            step3, step3_backup = get_place(query_result_next_page_2, api_key)
            data_last.extend(step3)
            data_backup.extend(step3_backup)

location_here = ['40.714995,-73.999377','40.737142,-73.990254', '40.737142,-73.990254', '40.737142,-73.990254','40.787547,-73.973355','40.809707,-73.945145', '40.844046,-73.938087']
# location_here = ['40.844046,-73.938087','40.729468,-74.001907','40.721933,-73.984630','40.750156,-73.997674','40.741722,-73.982002','40.763187,-73.990374',
# '40.756495,-73.973966','40.769730,-73.958458','40.778753,-73.980638','40.786639,-73.947667','40.794809,-73.969698','40.811598,-73.956659','40.803601,-73.940474',
# '40.825435, -73.944745','40.845696,-73.936173','40.865581,-73.923464','40.789728,-73.922949']
for i in location_here:
    print("Địa điểm đang crwal: ",i)
    get_info_business_by_googleApi('api_key',i)
    print("Done: ",i)
    print('--------------------------------------------------------------------------------')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

data_string = json.dumps(data_last, sort_keys=True, indent=4, cls=DecimalEncoder)
jj = open('manhattan_cafe.json', 'w')
jj.write(data_string)
jj.close()


data_string = json.dumps(data_backup, sort_keys=True, indent=4, cls=DecimalEncoder)
jj = open('manhattan_cafe_backup.json', 'w')
jj.write(data_string)
jj.close()