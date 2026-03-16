import redis
import gunicorn
from datetime import time
import time # for perf_counter
from urllib import parse
import encodings
import json
import os, sys
from pandas import DataFrame as df

# TODO: use python 3.6 (ADBDocs environment)
# because of Azure ML Studio support
# However, it doesn't work with Target

# This uses the Azure cache via stunnel
r = redis.Redis(host="localhost", port=6380, db=0, password='changeme')

def getClientLibStyles():
    styles = ''
    with open('ux/clientliib-site-v2.css') as f:
        styles = f.read()
    return styles

def KP_STYLESHEETS(pageName=None):
    if pageName == 'learn':
        return f'''
        <link rel="stylesheet" href="https://healthy.kaiserpermanente.org/etc.clientlibs/settings/wcm/designs/kporg/kp-foundation/clientlib-modules/styleguide.ec4bf16e2b4463638cb7d33583809dae.css" type="text/css" />
        <link rel="stylesheet" href="https://healthy.kaiserpermanente.org/etc.clientlibs/settings/wcm/designs/kporg/kp-foundation/clientlib-all.972a291a17b22239d3ca50c958d7fdff.css" type="text/css" />
        <link rel="stylesheet" href="https://healthy.kaiserpermanente.org/etc.clientlibs/settings/wcm/designs/kporg/kp-jkp-ptl/clientlib-all.da1ed0c388db819d04914c97cc3fde97.css" type="text/css"/>
        '''
    else:
        return f'''
            <style type="text/css">
            #{getClientLibStyles()}
            </style>
            <link rel="stylesheet" href="https://healthy.kaiserpermanente.org/etc.clientlibs/settings/wcm/designs/kporg/front-door/clientlib-all.df20d87ad43446af61ee6e57fbd1ff66.css" type="text/css" />
        '''

TARGET_PREHIDE_SCRIPT = '''
<script>
    //prehiding snippet for Adobe Target with asynchronous Launch deployment
    (function(g,b,d,f){(function(a,c,d){if(a){var e=b.createElement("style");e.id=c;e.innerHTML=d;a.appendChild(e)}})(b.getElementsByTagName("head")[0],"at-body-style",d);setTimeout(function(){var a=b.getElementsByTagName("head")[0];if(a){var c=b.getElementById("at-body-style");c&&a.removeChild(c)}},f)})(window,document,"body {opacity: 0 !important}",3E3);
</script>
'''

"""
Do a standard decoding of bytes to utf-8
"""
def sDecodeBytes(byts):
    return encodings.utf_8.decode(byts)[0] # ('<decoded_string>', length)

sContent = ''
hcContent = ''
with open("page_content.html") as f:
    sContent = f.read()

with open('page_content_basics_of_hc.html') as f:
    hcContent = f.read()


pKeys = {
    "5": "joe",
    "8": "sally",
    "7": "sal"
}

def app(environ, start_response):
    qs = parse.parse_qs(environ['QUERY_STRING'])
    print(f'''Path: {environ["PATH_INFO"]}''')
    # the default flag -> judy
    ident = qs.get('p', "1")
    if type(ident) == list:
        ident = ident[0]
    # TODO: grab the name dynamically from the payload returned
    if int(ident) < 10 and ident not in pKeys:
        name = "unknown"
    else:
        name = pKeys[ident]
    # get the redis call
    # b'1'
    # time just the redis calls
    tic = time.perf_counter()
    data = r.hget('f:ff', ident)
    hdp = r.hget('f:hdp', ident)
    md = json.loads(r.hget('p:metadata', ident))
    toc = time.perf_counter()
    print(f"profile: {ident}, who: {md['name']}\n")
    mrn = md['mrn']

    pageContent = sContent
    styleContent = KP_STYLESHEETS()
    # minimal routing
    if environ['PATH_INFO'] == '/learn/' or environ['PATH_INFO'] == '/learn':
        pageContent = hcContent
        styleContent = KP_STYLESHEETS('learn')

    page = bytes(f'''
    <!DOCTYPE HTML>
    <html lang="en-US">
        <head>
            <meta charset="utf-8" />
            {styleContent}
            {TARGET_PREHIDE_SCRIPT}
            <script src="//assets.adobedtm.com/6851bdae8e57/c70527835ccd/launch-9f669e6c50da-development.min.js" async></script>
            <script>
                window._dl = {{
                  'profile': {{
                    'id': '{md["id"]}',
                    'mrn': '{md["mrn"]}',
                    'region': '{md["region"]}',
                    'segments': {{
                        'ff': '{sDecodeBytes(data)}',
                        'hdp': '{sDecodeBytes(hdp)}',
                    }}
                  }}
                }}
                window.targetPageParams = function() {{
                    return {{
                         "profile": {{
                            "region": '{md["region"]}',
                            "ff": '{sDecodeBytes(data)}',
                            'hdp': '{sDecodeBytes(hdp)}',
                            "id": '{ident}',
                            "fname": '{name}'
                         }}
                    }}
                }}
            </script>
        </head>
        <body>
            {pageContent}
            <section id="debug">
            {name} : {sDecodeBytes(data)}<br />
            Redis call latency: {toc - tic:0.8f} seconds
            <section>
              <a href="/?p=8">Login as Sally, a non-ER Frequent Flyer (and ML-model physician-driven and computed indicators of heart disease)</a>
              <a href="/?p=5">Login as Joe, an ER Frequent Flyer (and has inferred indicators of heart disease)</a>
              <a href="/?p=1">Login as Mindy, someone with no indicators</a>
            </section>
            </section>
        </body>
    </html>
    ''', 'utf-8')

    start_response("200 OK", [
        ("Content-Type", "text/html"),
        ("Content-Length", str(len(page)))
    ])
    return iter([page])
