import foursquare
import ast
import urllib

client_id = "OCUL4KUN0I1JLF4HANT2HONTAK2ORB1FQOE3O5MGIFNBY25G"
client_secret = "25X3X2IRD01M4UWR4DPA1NC4DUUUOJ3NCDMBM1QT5SIKSLKB"
callback = 'http://localhost:8080/'

client = foursquare.Foursquare(access_token='DUXWBHZWHD2QHDJZKV15VHDK3FT2MWCNDYT42XZUTI5XRKCY')

foursquare_json_file = open('foursquare_json.txt', 'r')
complete_venues_foursquare_json_file = open('complete_venues_foursquare_json7.txt', 'a')

i_init = 9074
i_end = 9475
index = 0

for venue in foursquare_json_file:
    if index >= i_init:
        if i_init < i_end:
            venue_splited_line = venue.split()
            venue_index = venue_splited_line[0]
            venue_json_str = " ".join(venue_splited_line[1:])
            venue_json = ast.literal_eval(venue_json_str)

            result = client.venues(venue_json['id'])

            complete_venues_foursquare_json_file.write(str(venue_index) + ' ' + str(result) + '\n')

            i_init += 1
        else:
            break

    index += 1
