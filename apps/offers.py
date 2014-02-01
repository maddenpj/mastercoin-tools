import urlparse
import os, sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
from msc_utils_offerparsing import *
from msc_apps import *
import tempfile

def offers_response(response_dict):
    expected_fields=['address','currencyType','offerType']
    for field in expected_fields:
        if not response_dict.has_key(field):
            return (None, 'No field '+field+' in response dict '+str(response_dict))
        if len(response_dict[field]) != 1:
            return (None, 'Multiple values for field '+field)
    
    data = filterOffers(response_dict['address'][0],response_dict['currencyType'][0].upper(), response_dict['offerType'][0].upper() )    
    
    response_status='OK'
    response='{"status":"'+response_status+'", "data":'+ str(json.dumps(data)) +'}'
    return (response, None)

def filterOffers(address,currencytype, offertype):
    #      SELL OFFER OPTIONS
    # currencyType   =  TMSC or MSC
    # offerType      =  SELL, ACCEPT or BOTH
    
    
    #get list of all offers by address
    import json
    try:
        datadir = '/tmp/msc-webwallet/addr'
        filepath =  datadir + '/' + address + '.json'
        f=open( filepath , 'r' )
        allOffers = json.loads(f.readline())
    except IOError:
        return 'ADDRESS_NOT_FOUND'
    
    #filter by currency
    #1 is TMSC 
    #0 is MSC
    if currencytype != 'MSC':
        currency = '0'
    else:
        currency = '1'
    del allOffers[currency]
    
    #filter by offer type
    #accept_tx are offers accepted
    #bought_tx are offers bought
    #offer_tx are offers of sale
    #sold_tx are offers sold
    #recieved and sent tx are simple send
    #exodus tx is not related to offers
        
    #passingData = [address,currencytype, offertype, validitystatus, acceptstatus, salestatus]
        
    offerstruct = {}
    for key in allOffers:
        if isinstance(allOffers[key],dict):
            if offertype == 'BOTH':
                offerstruct['accept_tx'] = allOffers[key]['accept_transactions']
                offerstruct['bought_tx'] = allOffers[key]['bought_transactions']
                offerstruct['offer_tx'] = allOffers[key]['offer_transactions']
                offerstruct['sold_tx'] = allOffers[key]['sold_transactions']
                return offerstruct
            elif offertype == 'ACCEPT': #accept_tx
                offerstruct['accept_tx'] = allOffers[key]['accept_transactions']
                offerstruct['bought_tx'] = allOffers[key]['bought_transactions']
                return offerstruct
            elif offertype == 'SELL': #offer_tx
                offerstruct['offer_tx'] = allOffers[key]['offer_transactions']
                offerstruct['sold_tx'] = allOffers[key]['sold_transactions']
                return offerstruct


def offers_handler(environ, start_response):
    return general_handler(environ, start_response, offers_response)
