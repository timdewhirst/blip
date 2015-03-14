
import os
import os.path
import requests
import sys
import json
import time

baseendpoint='https://api.polaroidblipfoto.com/4/'
accesstoken='305411915fa8ab4f0d4bf0a3bb2e38968f0a8d1a'

# need either entry_id or username
def getData( params, basedir ):
    params.update(
        { 'return_details': 1,
          'return_metadata': 1,
          'return_comments': 1,
          'include_replies': 1,
          'return_related': 1
        } )
    
    r=requests.get(baseendpoint+'entry', params=params, headers={'Authorization':'Bearer '+accesstoken})
    if r.status_code != requests.codes.ok:
        print( "failed to fetch data: {0}".format( r.status_code ) )
        exit( 1 )

    m=r.json();
    entryid=m['data']['entry']['entry_id_str']
    previd=None
    if "previous" in m['data']['related'].keys():
        previd=m['data']['related']['previous']['entry_id_str']
    imgurl=m['data']['entry']['image_url']
    print( "entry id: {0}, {1}".format( entryid, imgurl ) )

    savedir=os.path.join( basedir, entryid )
    if not os.path.exists( savedir ):
        os.mkdir( savedir )

        # save the content
        fid=open( os.path.join( savedir, "content.json" ), "w+" )
        fid.write( r.text )
        fid.close()

        # go and get the image
        r=requests.get(imgurl, headers={'Authorization':'Bearer '+accesstoken})
        if r.status_code != requests.codes.ok:
            print( "failed to fetch image: {0}".format( r.status_code ) )
        else:
            fid=open( os.path.join( savedir, "image.jpg" ), "wb" )
            fid.write( r.content )
            fid.close()

        print( "saved content and image!" )
    else:
        print( "looks like you already have this entry; skipping..." )

    if previd is None:
        print( "no more entries" )
        exit( 0 )

    time.sleep( 2 )
    getData( { 'entry_id': previd }, basedir )
        
    
def main( argv ):
    if len( argv ) < 2:
        print( "usage: {0} <username> [first entry id]".format( argv[0] ) )
        exit( 1 )

    # okay, let's go! start from most recent and work backwards
    username=argv[1]
    if not os.path.exists( username ):
        os.mkdir( username )

    initialq={'username': username}
    if len( argv ) == 3:
        initialq={'entry_id': argv[2]}

    getData( initialq, username )

if __name__ == "__main__":
    main( sys.argv )
