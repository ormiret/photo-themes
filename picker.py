from flask import Flask, render_template, jsonify, request, json, redirect
from StringIO import StringIO
import gzip
import urllib2
import random
import os

app = Flask(__name__)

################################################################################
#                             _               _   _    _                       #
#                _ _ ___ _ __| |__ _ __ ___  | |_| |_ (_)___                   #
#               | '_/ -_) '_ \ / _` / _/ -_) |  _| ' \| (_-<                   #
#               |_| \___| .__/_\__,_\__\___|  \__|_||_|_/__/                   #
#                       |_|                                                    #
################################################################################
header = """
User-Agent: Mozilla/5.0 (X11; FreeBSD amd64; rv:49.0) Gecko/20100101 Firefox/49.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
X-CSRF-Token: J2iawi/G7GJ3cqXgKVhYVlIQjNMWCXCdSPNscW/lyZb0xk1+Y3HWlPgCW6/kYQWY6tkfSWF2IWDtx8H8Q8A4Eg==
Referer: https://500px.com/search?type=photos&utm_campaign=google_search_box&q=blue
Origin: https://500px.com
Cookie: _hpx1=BAh7CkkiD3Nlc3Npb25faWQGOgZFVEkiJTcwNWJhODM3OGE0ODIwZGRjMWMzNzBmZGY5NGU1ZTczBjsAVEkiCWhvc3QGOwBGIg41MDBweC5jb21JIhhzdXBlcl9zZWNyZXRfcGl4M2xzBjsARkZJIhBfY3NyZl90b2tlbgY7AEZJIjEwNjdYdkV5M092YVBjUDVQelRsZHpyakprNXAzZjFIOXBUU3RqU3dsOFlRPQY7AEZJIhFwcmV2aW91c191cmwGOwBGSSI%2BL3NlYXJjaD90eXBlPXBob3RvcyZ1dG1fY2FtcGFpZ249Z29vZ2xlX3NlYXJjaF9ib3gmcT1ibHVlBjsAVA%3D%3D--2a92d13e5bc840dd0de0d3d469d0cc3019e12fb3; optimizelyEndUserId=oeu1478624905590r0.6262684177302974; optimizelySegments=%7B%22569090246%22%3A%22false%22%2C%22569491641%22%3A%22campaign%22%2C%22575800731%22%3A%22ff%22%2C%22589900200%22%3A%22true%22%7D; optimizelyBuckets=%7B%227781310076%22%3A%227773970029%22%7D; _ga=GA1.2.166996737.1478624906; _gat=1; _gat_unifiedTracker=1; amplitude_id500px.com=eyJkZXZpY2VJZCI6IjJkYjljZTg3LTk5ZjktNDg4Yy1hNTFlLWNhN2M5ZGU3MGUwZFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTQ3ODYyNDkzMTM1NSwibGFzdEV2ZW50VGltZSI6MTQ3ODYyNDkzMTM1NSwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9; optimizelyPendingLogEvents=%5B%22n%3Dhttps%253A%252F%252F500px.com%252Fsearch%253Ftype%253Dphotos%2526utm_campaign%253Dgoogle_search_box%2526q%253Dblue%26u%3Doeu1478624905590r0.6262684177302974%26wxhr%3Dtrue%26time%3D1478624986.482%26f%3D7763794202%2C7254840151%2C7769081978%2C7513516222%2C7781310076%26g%3D582890389%22%5D
Connection: keep-alive
Cache-Control: max-age=0
"""
################################################################################

host = "api.500px.com"
path = "/v1/photos/search?type=photos&term={}&image_size%5B%5D=1&image_size%5B%5D=2&image_size%5B%5D=32&image_size%5B%5D=31&image_size%5B%5D=33&image_size%5B%5D=34&image_size%5B%5D=35&image_size%5B%5D=36&image_size%5B%5D=2048&image_size%5B%5D=4&image_size%5B%5D=14&include_states=true&formats=jpeg%2Clytro&include_tags=true&exclude_nude=true&page=1&rpp=50"

themes_url="https://raw.githubusercontent.com/ormiret/photo-themes/master/themes.txt"

def search500px(searchstring):
    query = urllib2.quote(searchstring)

    url = "https://" + host + path.format(query)

    opener = urllib2.build_opener()
    for line in header.split("\n"):
        if not line: 
            continue

        s = line.split(":") 
        opener.addheaders.append((s[0], s[1].strip()))

    response = opener.open(url)

    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()

    data = json.loads(data)
    photos = data["photos"]
    print("{} photos in response".format(len(photos)))

    images = [] 
    for photo in photos:
        image = photo["image_url"][-1]
        page_url = "https://500px.com/" + photo["url"]

        images.append({"image":image, "page_url":page_url})
    return images

THEMES = os.path.join(os.path.dirname(__file__), "themes.txt")

def rand_line(filename):
    with open(filename) as f:
        lines = f.readlines()
    return unicode(random.choice(lines).strip(), "utf-8")

@app.route("/")
def cah_filled():
    searchstring = rand_line(THEMES)
    return render_template("theme.html", 
        theme=searchstring, images=search500px(searchstring))

@app.route("/theme.json")
def cah_json():
    return jsonify({"theme":rand_line(THEMES)})

