# import pyfoursquare as foursquare
# # == OAuth2 Authentication ==
# #
# # This mode of authentication is the required one for Foursquare
#
# # The client id and client secret can be found on your application's Details
# # page located at https://foursquare.com/oauth/
# client_id = "OCUL4KUN0I1JLF4HANT2HONTAK2ORB1FQOE3O5MGIFNBY25G"
# client_secret = "25X3X2IRD01M4UWR4DPA1NC4DUUUOJ3NCDMBM1QT5SIKSLKB"
# callback = 'http://localhost:8080/'
#
# auth = foursquare.OAuthHandler(client_id, client_secret, callback)
#
# #First Redirect the user who wish to authenticate to.
# #It will be create the authorization url for your app
# auth_url = auth.get_authorization_url()
# print 'Please authorize: ' + auth_url
#
# #If the user accepts, it will be redirected back
# #to your registered REDIRECT_URI.
# #It will give you a code as
# #https://YOUR_REGISTERED_REDIRECT_URI/?code=CODE
# code = raw_input('The code: ').strip()
#
# #Now your server will make a request for
# #the access token. You can save this
# #for future access for your app for this user
# access_token = auth.get_access_token(code)
# print 'Your access token is ' + access_token
#
# #Now let's create an API
# api = foursquare.API(auth)
#
# #Now you can access the Foursquare API!
# result = api.venues_search(query='Burburinho', ll='-8.063542,-34.872891')
#
# #You can acess as a Model
# print dir(result[0])
#
# #Access all its attributes
# print result[0].name
#
# # access token = DUXWBHZWHD2QHDJZKV15VHDK3FT2MWCNDYT42XZUTI5XRKCY