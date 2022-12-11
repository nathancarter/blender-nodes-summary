
import warnings
import json
import requests
from bs4 import BeautifulSoup

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}
OUT_FILE = 'scraped_data.json'

def make_soup ( url ):
    with warnings.catch_warnings():
        warnings.simplefilter( 'ignore' )
        return BeautifulSoup( requests.get( url, headers, verify=False ).content, 'lxml' )

def get_image_url ( url ):
    node_page = make_soup( url )
    body = node_page.find( itemprop='articleBody' )
    if not body:
        return
    section = body.find( 'section' )
    if not section:
        return
    image = body.find( 'img' )
    if not image:
        return
    return '/'.join( url.split( '/' )[:-1] ) + '/' + image.get( 'src' )

def all_nodes_at_url ( outer_url ):
    nodes_page = make_soup( outer_url )
    node_type_sect = nodes_page.find( id='node-types' ) \
                  or nodes_page.find( id='shader-nodes' )
    all_links = node_type_sect.find_all( **{'class':'reference internal'} )
    result = [ ]
    print( f'Starting {outer_url}')
    for ( i, link ) in enumerate( all_links ):
        url = link.get( 'href' )
        if url.endswith( '/index.html' ):
            result.append( {
                'title' : link.text,
                'url' : url + link.get( 'href' ),
                'contents' : [ ]
            } )
        else:
            node_page_url = outer_url + link.get( 'href' )
            image_url = get_image_url( node_page_url )
            if image_url:
                result[-1]['contents'].append( {
                    'page' : node_page_url,
                    'image' : image_url
                } )
        if i > 0 and i % 10 == 0:
            print( f'Scraped {100*(i+1)/len(all_links):3.1f}% of {outer_url}' )
    print( f'Finished {outer_url}')
    return result

scraped_data = { }
for url in [
    'https://docs.blender.org/manual/en/latest/render/shader_nodes/',
    'https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/'
]:
    scraped_data[url] = all_nodes_at_url( url )
with open( OUT_FILE, 'w' ) as f:
    json.dump( scraped_data, f )

print( 'Done.' )
