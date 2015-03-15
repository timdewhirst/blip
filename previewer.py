
import os
import os.path
import requests
import sys
import json
import time

# fill me in!
# get your own app credentials from here:
# https://www.polaroidblipfoto.com/developer/api (see README.md)
baseendpoint=''
accesstoken=''

# get and save an image
def getAndSaveImage( url, accesstoken, savedir, name ):
    # go and get the image
    r=requests.get(url, headers={'Authorization':'Bearer '+accesstoken})
    if r.status_code != requests.codes.ok:
        print( "failed to fetch image: {0}".format( r.status_code ) )
    else:
        fid=open( os.path.join( savedir, name ), "wb" )
        fid.write( r.content )
        fid.close()
    

# need either entry_id or username
def getData( params, basedir ):
    params.update(
        { 'return_details': 1,
          'return_metadata': 1,
          'return_comments': 1,
          'include_replies': 1,
          'return_related': 1,
          'return_image_urls': 1
        } )

    # make the request; extract the JSON
    r=requests.get(baseendpoint+'entry', params=params, headers={'Authorization':'Bearer '+accesstoken})
    if r.status_code != requests.codes.ok:
        print( "failed to fetch data: {0}".format( r.status_code ) )
        exit( 1 )

    m=r.json();

    # extract the information we're interested in
    try:   
        entryid=str(m['data']['entry']['entry_id'])
        previd=None
        if m['data']['related']['previous'] != None:
            previd=str(m['data']['related']['previous']['entry_id'])
        imgurl=m['data']['entry']['image_url']
        thumburl=m['data']['entry']['thumbnail_url']
        print( "entry id: {0}, {1}".format( entryid, imgurl ) )

        savedir=os.path.join( basedir, entryid )
        if not os.path.exists( savedir ):
            os.mkdir( savedir )

            # save the content
            fid=open( os.path.join( savedir, "content.json" ), "w+" )
            fid.write( r.text )
            fid.close()

            # go and get the images
            getAndSaveImage( imgurl, accesstoken, savedir, "image.jpg" )
            getAndSaveImage( thumburl, accesstoken, savedir, "thumbnail.jpg" )
            
            print( "saved content and image!" )
        else:
            print( "looks like you already have this entry; skipping..." )

        if previd == None:
            print( "no more entries!" )
            return
    
    except:
        print( "got an error: {0}".format( r.json() ) )
        raise

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
