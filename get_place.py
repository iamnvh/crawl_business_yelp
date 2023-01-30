def get_place(query_result, api_key):
    result_backup = []
    result = []
    for place in query_result.places:
        try:
            place.get_details()
            details = place.details
            if details['user_ratings_total'] > 10 and details['business_status'] == 'OPERATIONAL':
                data = {}
                weekday = details['opening_hours']['weekday_text']
                item = []
                for i in weekday:
                    businessHour = i.split(': ')[1].strip()
                    if businessHour == 'Open 24 hours':
                        item.append([{
                            'open': '0000',
                            'close': '2359'
                        }])
                    elif businessHour == 'Closed':
                        item.append([{
                            'open': None,
                            'close': None
                        }])
                    else :
                        if ',' in businessHour:
                            shift = businessHour.split(',')
                            item_child = []
                            for i in shift:
                                open = i.split('\u2009\u2013\u2009')[0]
                                if '\u202f' in open:
                                    open_value = open.split('\u202f')[0]
                                    open_suffix = open.split('\u202f')[1]
                                else:
                                    open_value = open
                                    open_suffix = 'AM'
                                close = i.split('\u2009\u2013\u2009')[1]
                                if '\u202f' in close:
                                    close_value = close.split('\u202f')[0]
                                    close_suffix = close.split('\u202f')[1]
                                else:
                                    close_value = close
                                    close_suffix = 'AM'


                                if open_suffix ==  'PM' :
                                    open_value = str(int(open_value.split(':')[0]) + 12) + open_value.split(':')[1]
                                    if len(open_value) == 3:
                                        open_value = '0'+ open_value
                                else:
                                    open_value = str(int(open_value.split(':')[0])) + open_value.split(':')[1]
                                    if len(open_value) == 3:
                                        open_value = '0'+ open_value

                                if close_suffix ==  'PM' :
                                    close_value = str(int(close_value.split(':')[0]) + 12) + close_value.split(':')[1]
                                    if len(close_value) == 3:
                                        close_value = '0'+ close_value
                                
                                else:
                                    close_value = str(int(close_value.split(':')[0])) + close_value.split(':')[1]
                                    if len(close_value) == 3:
                                        close_value = '0'+ close_value
                                    
                                item_child.append([{
                                    'open': open_value,
                                    'close': close_value
                                }])
                            item.append(item_child)
                        else:
                            open = businessHour.split('\u2009\u2013\u2009')[0]
                            if '\u202f' in open:
                                    open_value = open.split('\u202f')[0]
                                    open_suffix = open.split('\u202f')[1]
                            else:
                                open_value = open
                                open_suffix = 'AM'
                            close = businessHour.split('\u2009\u2013\u2009')[1]
                            if '\u202f' in close:
                                    close_value = close.split('\u202f')[0]
                                    close_suffix = close.split('\u202f')[1]
                            else:
                                close_value = close
                                close_suffix = 'AM'
                            
                            if open_suffix ==  'PM' :
                                open_value = str(int(open_value.split(':')[0]) + 12) + open_value.split(':')[1]
                                if len(open_value) == 3:
                                    open_value = '0'+ open_value
                            else:
                                open_value = str(int(open_value.split(':')[0])) + open_value.split(':')[1]
                                if len(open_value) == 3:
                                    open_value = '0'+ open_value

                            if close_suffix ==  'PM' :
                                close_value = str(int(close_value.split(':')[0]) + 12) + close_value.split(':')[1]
                                if len(close_value) == 3:
                                    close_value = '0'+ close_value
                            
                            else:
                                close_value = str(int(close_value.split(':')[0])) + close_value.split(':')[1]
                                if len(close_value) == 3:
                                    close_value = '0'+ close_value
                                
                            
                            item.append([{
                                'open': open_value,
                                'close': close_value
                            }])

                data['businessHours'] = item     
                data['geolocation'] = {
                    "latitude": place.geo_location['lat'],
                    "longitude": place.geo_location['lng']
                }
                data['businessName'] = place.name
                data['businessAddress'] = place.formatted_address
                data['businessType'] = "Restaurant"
                data['localPhoneNumber'] = place.local_phone_number
                data['internationalPhoneNumber'] = place.international_phone_number
                data['thumbnailUrl'] = 'https://maps.googleapis.com/maps/api/place/photo?photoreference='+details['photos'][0]['photo_reference']+'&sensor=false&maxheight=500&maxwidth=500&key='+api_key
                result.append(data)
                result_backup.append(details)
        except:
            pass
    return result, result_backup
