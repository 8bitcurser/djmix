# djmix
Dj mix is a simple python tool that migrates your favorite artists from Spotify to Youtube Music

## Obtaining your keys

### Spotify 

Extract your spotify token from their official developers site: https://developer.spotify.com, copy the token from the code snippet generated there.
If you dont see a token you need to login with your spotify credentials on that site, then when you go back to it the token will be shown on the snippet.
Add them to the `keys.json` file under the key 'spotify'

Things to notice, the api key will expire after some time. So you might need to re generate it by doing the same steps as before.

### Youtube Music

Open the developer tools on your browser, go to the networks tab and filter the results by XHR. Then head to the search bar and look for whatever artist you want,
Look for the search request and for the Cookie header, copy the value from the Cookie header and paste it on `keys.json` under the key 'ytmusic_cookie'

## How long can it take?

It takes some time as there is no official youtube music api and ytmusic api library doesn't provide a way for us to get the channel id needed to generate a subscription,
so we need to make manual requests as if we were a browser and parse the response, so grab a coffee and wait!


## How To run

1. Install poetry
2. Run `poetry install`
3. Run `poetry run python3 main.py`
4. Enjoy!