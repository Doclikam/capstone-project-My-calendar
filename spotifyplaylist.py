"""
understanding how Oauth works:
oAuth is used to authenticate API requests.
first step is to request authorization from the user so that our app can access to the Spotify resources on the user's behalf.
To do this, our application must build and send a GET request to the /authorize endpoint with the following parameters:

1. client_id
2. response_type: set this to 'code'
3.redirect_uri
4.scope
5.state
6.show_dialog


"""
from flask import Flask, redirect, jsonify, request, session
from datetime import datetime, timedelta


import requests
import urllib.parse




#initializing flask apllication
app=Flask(__name__)

app.config['SESSION_COOKIE_NAME']='Spotify cookie'
app.secret_key="45dddrt-569b-4668-a556-1f56778909"

CLIENT_ID='7f6b402d2a8c480aa244cd87f64bbdb8'
CLIENT_SECRET='1cf23b8d2e994dafb7cf867b08ccda7a'
REDIRECT_URI="http://localhost:5000/callback"


AUTH_URL='https://accounts.spotify.com/authorize/?'
TOKEN_URL='https://accounts.spotify.com/api/token'
BASE_URL='https://api.spotify.com'

#when user in the page the name allows them to be redirected to the login page
@app.route('/')
#function to redirect uder to a login link endpoint
def index():
    return "Welcome to My Music Player <a href='/login'>login with spotify </a>"


#creating a login endpoint
@app.route('/login')
def login():
    #the scope will allow the app to read the users data
    scope='user-read-private playlist-modify-public user-read-email'

    #setting parameters required 
    parameters={
        'client_id':CLIENT_ID,
        'response_type': 'code',
        'scope':scope,
        'redirect_uri': REDIRECT_URI}


    oAuth_url=f"{AUTH_URL}?{urllib.parse.urlencode(parameters)}"


    return redirect(oAuth_url)

#callback for API to return to when the user logs in
@app.route('/callback')
def redirect_user():
    
    #handling error if 
    if 'error' in request.args:
        return jsonify({'error': request.args['error']})

    #if the auth'code' is in request sent, then the oAuth wull be returned for an access token  
    if 'code' in request.args:
        request_info={
            'code': request.orgs['code'],
            'grant_type':'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id':CLIENT_ID,
            'client_secret': CLIENT_SECRET}
        
        response=requests.post(TOKEN_URL, data=request_info)
        #the token can then be stored in this varible
        token_info=response.json()


        #the token info can then be stored in the session
        session['access_token']=token_info['access_token']
        session['refresh_token']=token_info['refresh_token']
        session['expired_at']=datetime.now().timestamp()+token_info['expires_in']


        return redirect('/playlists')




app.route('/playlists')

#getting playlists
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')


    if datetime.now().timestamp()>session['expired_at']:
        return redirect('/refresh.token')


    headers={'Authorization':f"Bearer{[access_token]}"
    }
    response=requests.get(API_BASE_URL+'me/playlists', headers=headers)

    playlists=response.json()

    return jsonify(playlists)

app.route('refresh-token')
def refresh_token():
    if refresh_token not in session:
        return redirect('/login')

    #if the token has expired then a fresh token should be generated
    if datetime.now().timestamp()>session['expired_at']:
        required_info={
        'grant_type':'refresh_token', 
        'refresh_token':session['refresh_token'],
        'client_id':CLIENT_ID,
        'client_secret': CLIENT_SECRET
        }


        response=request.post(TOKEN_URL, data=required_info)
        new_token_info=response.json()

        #we can overwrite the old token with an new token 
        session['access_token']=new_token_info['access_token']
        #we can now get a new expiry time for the token
        session['expired_at']=datetime.now().timestamp()+new_token_info['expires_in']

#running flask on our local host
if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True)


