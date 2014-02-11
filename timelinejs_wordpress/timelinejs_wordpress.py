# coding=utf-8

import requests, csv, tempfile, json
from dateutil import parser
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

WP_URL = "http://timeline.pravonagrad.org/"
WP_USERNAME = "admin"
WP_PASSWORD = "******"
WP = Client(WP_URL + "xmlrpc.php", WP_USERNAME, WP_PASSWORD)

CSV_URL = "https://docs.google.com/spreadsheet/pub?key=0AjZc5ivkNPGTdFEzSWR6aFZnTTJCY2EyVzlhaGQxdVE&output=csv"

TIMELINE_JSON = {}

def get_csv_dict():
    req = requests.get(CSV_URL)
    with tempfile.NamedTemporaryFile() as fajl:
        fajl.write(req.content)
        return csv.DictReader(open(fajl.name), delimiter=",", quotechar = '"')

def prepare_post(event):
    post = WordPressPost()
    post.title = event['Headline']
    body_string = '''<p id="pagekeeper"><img src='http://free.pagepeeker.com/v2/thumbs.php?size=x&url={}'><br/>{}</p><p>{}</p>'''.format(event["Media"], event["Media Credit"].replace("\n", ""), event["Text"])
    post.content = body_string
    post.date = parser.parse(event['Start Date'])
    post.terms_names = {'post_tag': [event['Tag']]}
    post.post_status = 'publish'
    return post

def publish_post(post):
    post_id = WP.call(NewPost(post))
    return (post, post_id)

def write_csv(ev_dict, file_name = "/tmp/events_dict.csv"):
    output_csv = csv.DictWriter(open(file_name, "wb"), fieldnames=events_dict.fieldnames)
    output_csv.writeheader()
    output_csv.writerows(ev_dict)

def publish_events(n,m):
    global events
    for i in range(n,m):
        p = prepare_post(events[i])
        po, pi = publish_post(p)
        pi = i
        events[i]['Headline'] = '<a href="{}?p={}" target="png_wp_posts" id="tl_headline">{}</a>'.format(WP_URL, str(pi), events[i]['Headline'])

def write_json(events):
    global TIMELINE_JSON
    TIMELINE_JSON["timeline"] = {
    "headline" : "Pravo na grad - arhiva",
    "type" : "default",
        "text" : "<p>Na ovim stranicama dokumentirane su aktivnosti Prava na grad u periodu od ožujka 2006 do travnja 2011 godine. Najvažniji događaji prikazani su na vremenskoj crti, a pripadajući arhivski dokumenti pridruženi su svakom događaju. Svaki događaj pridružen je kontekstu različitih aktera: Pravo na grad i Zelena akcija, investitor (HOTO), grad Zagreb, mediji i drugi institucionalni akteri.</p>",
    "asset": {
        "media": "http://www.pravonagrad.org",
        "credit" : "...",
        "caption" : "Caption text goes here"}
    }
    TIMELINE_JSON["timeline"]["date"] = []
    for event in events:
        TIMELINE_JSON["timeline"]["date"].append({
            "startDate" : parser.parse(event["Start Date"]).strftime("%m/%d/%Y"),
            "endDate" : parser.parse(event["End Date"]).strftime("%m/%d/%Y"),
            "headline" : event["Headline"],
            "text" : event["Text"],
            "tag" : event["Tag"],
            "classname" : "timeline_class",
            "asset" : {
                "media" : event["Media"],
                "thumbnail" : event["Media Tumbnail"],
                "credit" : event["Media Credit"],
                "caption" : event["Media Caption"]}
        })

events_dict = get_csv_dict()
events = [event for event in events_dict]
publish_events(0,len(events)-1)
write_json(events)
json.dump(TIMELINE_JSON, open("/tmp/timeline.json", "wb"))
