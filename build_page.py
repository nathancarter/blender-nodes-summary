
import json

IN_FILE = 'scraped_data.json'
OUT_FILE = 'index.html'

with open( IN_FILE, 'r' ) as f:
    scraped_data = json.load( f )

html = '''
<html>
    <head>
        <style>
            img {
                width: 200px;
                vertical-align: top;
            }
            body {
                background-color: black;
            }
            a {
                color: white;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
'''

for node_type_url in scraped_data.keys():
    node_type = node_type_url[:-1].split( '/' )[-1].replace( '_', ' ' ).title()
    html += '        <hr/>\n'
    html += f'        <h1><a href="{node_type_url}">{node_type}</a></h1>\n'
    for section in scraped_data[node_type_url]:
        html += '        <hr/>\n'
        html += f'        <h2><a href="{section["url"]}">{section["title"]}</a></h2>\n'
        for data in section['contents']:
            if data["image"].startswith( 'http' ):
                html += f'        <a href="{data["page"]}"><img src="{data["image"]}"/></a>\n'
            else:
                html += f'        <p><a href="{data["page"]}">{data["image"]}</a></p>\n'

html += '    </body>\n</html>'

with open( OUT_FILE, 'w' ) as f:
    f.write( html )
