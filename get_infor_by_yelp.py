
from decimal import *
import requests
from bs4 import BeautifulSoup
import requests, json, urllib, random, time

def get_nominatim_geocode(address):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'
    response = requests.get(url).json()
    data = {
        "latitude": response[0]["lat"],
        "longitude": response[0]["lon"]
    }
    return data

def GET_UA():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
                ]
 
    return random.choice(uastrings)

def get_info(link, b_type):
    try:
        data = {}
        headers = {'User-Agent': GET_UA()}
        html = requests.get(link, headers=headers).content
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find('h1', class_='css-1se8maq').text
        data['businessName'] = name
        address = ' '.join([str(elem.text) for elem in soup.find('address').find_all('span')])
        data['businessAddress'] = address
        img_link = soup.find('a', 'photo-header-media-link__09f24__xmWtR css-1sie4w0').find('img')['src']
        data['thumbnailUrl'] = img_link
        check_phone = soup.find_all('div', 'css-1vhakgw')
        phone = ''
        for i in check_phone:
            try:
                if i.find('p', class_='css-na3oda').text == 'Phone number':
                    phone = i.find('p', class_='css-1p9ibgf').text
            except: pass
        if phone == '':
            data['phoneNumber'] = None
        else:
            data['phoneNumber'] = phone
        try:
            lat_lng = str(soup.find('div', class_='container__09f24__fZQnf').find('img')['src']).split('center=')[1].split('&')[0]
            data['geolocation'] = {
                "latitude": lat_lng.split('%2C')[0],
                "longitude": lat_lng.split('%2C')[1]
            }
        except:
            lat_lng = get_nominatim_geocode(address)
            data['geolocation'] = lat_lng
        data['businessType'] = b_type
        open_hours = soup.find_all('tr',class_='css-29kerx')
        shift_day = []
        for index, i in enumerate(open_hours):
            if index % 2 == 0:
                continue
            day = i.find('ul').find_all('li')
            if len(day) > 1:
                shift = []
                if day[0].text == 'Closed':
                    shift.append({
                        'open': None,
                        'close': None
                    })
                else :
                    first_shift = day[0].text
                    open_value_first_shift = first_shift.split('-')[0].strip().split(' ')[0]
                    open_suffix_first_shift = first_shift.split('-')[0].strip().split(' ')[1]
                    if open_suffix_first_shift == 'PM':
                        open_value_first_shift = str(int(open_value_first_shift.split(':')[0]) + 12) + open_value_first_shift.split(':')[1]
                        if len(open_value_first_shift) == 3:
                            open_value_first_shift = '0'+open_value_first_shift
                    else:
                        open_value_first_shift = open_value_first_shift.replace(':','')
                        if len(open_value_first_shift) == 3:
                            open_value_first_shift = '0'+open_value_first_shift
                    close_value_first_shift = first_shift.split('-')[1].strip().split(' ')[0]
                    close_suffix_first_shift = first_shift.split('-')[1].strip().split(' ')[1]
                    if close_suffix_first_shift == 'PM':
                        close_value_first_shift = str(int(close_value_first_shift.split(':')[0]) + 12) + close_value_first_shift.split(':')[1]
                        if len(close_value_first_shift) == 3:
                            close_value_first_shift = '0'+close_value_first_shift
                    else:
                        close_value_first_shift = close_value_first_shift.replace(':','')
                        if len(close_value_first_shift) == 3:
                            close_value_first_shift = '0'+close_value_first_shift
                    shift.append({
                        'open': open_value_first_shift,
                        'close': close_value_first_shift
                    })
                if day[1].text == 'Closed':
                    shift.append({
                        'open': None,
                        'close': None
                    })
                else:
                    second_shift = day[1].text
                    open_value_second_shift = second_shift.split('-')[0].strip().split(' ')[0]
                    open_suffix_second_shift = second_shift.split('-')[0].strip().split(' ')[1]
                    if open_suffix_second_shift == 'PM':
                        open_value_second_shift = str(int(open_value_second_shift.split(':')[0]) + 12) + open_value_second_shift.split(':')[1]
                        if len(open_value_second_shift) == 3:
                            open_value_second_shift = '0'+open_value_second_shift
                    else:
                        open_value_second_shift = open_value_second_shift.replace(':','')
                        if len(open_value_second_shift) == 3:
                            open_value_second_shift = '0'+open_value_second_shift
                    close_value_second_shift = second_shift.split('-')[1].strip().split(' ')[0]
                    close_suffix_second_shift = second_shift.split('-')[1].strip().split(' ')[1]
                    if close_suffix_second_shift == 'PM':
                        close_value_second_shift = str(int(close_value_second_shift.split(':')[0]) + 12) + close_value_second_shift.split(':')[1]
                        if len(close_value_second_shift) == 3:
                            close_value_second_shift = '0'+close_value_second_shift
                    else:
                        close_value_second_shift = close_value_second_shift.replace(':','')
                        if len(close_value_second_shift) == 3:
                            close_value_second_shift = '0'+close_value_second_shift

                    shift.append({
                        'open': open_value_second_shift,
                        'close': close_value_second_shift
                    })
                
                shift_day.append(shift)
            else :
                shift = []
                if day[0].text == 'Closed':
                    shift.append({
                        'open': None,
                        'close': None
                    })
                else:
                    first_shift = day[0].text
                    open_value_first_shift = first_shift.split('-')[0].strip().split(' ')[0]
                    open_suffix_first_shift = first_shift.split('-')[0].strip().split(' ')[1]
                    if open_suffix_first_shift == 'PM':
                        open_value_first_shift = str(int(open_value_first_shift.split(':')[0]) + 12) + open_value_first_shift.split(':')[1]
                        if len(open_value_first_shift) == 3:
                            open_value_first_shift = '0'+open_value_first_shift
                    else:
                        open_value_first_shift = open_value_first_shift.replace(':','')
                        if len(open_value_first_shift) == 3:
                            open_value_first_shift = '0'+open_value_first_shift
                    close_value_first_shift = first_shift.split('-')[1].strip().split(' ')[0]
                    close_suffix_first_shift = first_shift.split('-')[1].strip().split(' ')[1]
                    if close_suffix_first_shift == 'PM':
                        close_value_first_shift = str(int(close_value_first_shift.split(':')[0]) + 12) + close_value_first_shift.split(':')[1]
                        if len(close_value_first_shift) == 3:
                            close_value_first_shift = '0'+close_value_first_shift
                    else:
                        close_value_first_shift = close_value_first_shift.replace(':','')
                        if len(close_value_first_shift) == 3:
                            close_value_first_shift = '0'+close_value_first_shift

                    shift.append({
                        'open': open_value_first_shift,
                        'close': close_value_first_shift
                    })
                shift_day.append(shift)
        if len(shift_day) != 0:
            data['businessHours'] = shift_day
        else:
            businesshours_null = []
            for i in range(7):
                businesshours_null.append([{
                'open': None,
                'close': None
            }])
            data['businessHours'] = businesshours_null
        return data
    except:
        pass


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def run(file_name_links, file_name_ouput, business_type):
    result = []
    links = open(file_name_links, 'r', encoding='utf-8')
    links = links.read().splitlines()
    for index, i in enumerate(links):
        if index == 50:
            time.sleep(10)
        print('Crawl loading form link : ',index+1)
        data = get_info(i, business_type)
        if data:
            result.append(data)
            print("Crawl done link: ", index+1)
    
    data_json = json.dumps(result, sort_keys=True, indent=4, cls=DecimalEncoder)
    save_data = open(file_name_ouput, 'w')
    save_data.write(data_json)
    save_data.close()


run('yelp.txt','beauty_salon_brooklyn.json','Beauty Salon')