import urlparse
import os, sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
from msc_utils_offerparsing import *
from msc_apps import *
import tempfile

def offers_response(response_dict):
    expected_fields=['address','currencyType','offerType','validityStatus','acceptsStatus','salesStatus']
    for field in expected_fields:
        if not response_dict.has_key(field):
            return (None, 'No field '+field+' in response dict '+str(response_dict))
        if len(response_dict[field]) != 1:
            return (None, 'Multiple values for field '+field)
    print response_dict        
    data = sortdata(response_dict['address'][0],response_dict['currencyType'][0].upper(), response_dict['offerType'][0].upper(), response_dict['validityStatus'][0].upper(), response_dict['acceptsStatus'][0].upper(), response_dict['salesStatus'][0].upper())    
    
    response_status='OK'
    response='{"status":"'+response_status+'", "data":"'+ data +'"}'
    return (response, None)

def sortdata(address,currencytype, offertype, validitystatus, acceptstatus, sale_status):
    #    SELL OFFER OPTIONS     |  ACCEPT OFFER OPTIONS
    # currencyType   =  TMSC or MSC
    # offerType      =  SELL or ACCEPT
    # validityStatus =  VALID, INVALID, EXPIRED or ANY
    # acceptsStatus  =  [NONE, SOME, CLOSED, or ANY], [N/A]
    # sale_status    =  [NONE, SOME, CLOSED, or ANY], [WAITING, PAID, N/A]
    
    passingData = [address, offertype, validitystatus, acceptstatus, sale_status]
    
    #get list of all offers by address
    allOffers = getOffers(address)
    if allOffers != 'no such address':
        currencyFilteredOffers = filterOffers_byCurrency(allOffers, currencytype)
        typeFilteredOffers = filterOffers_byType(currencyFilteredOffers, offertype)
        statusFilteredOffers = filterOffers_byStatus(typeFilteredOffers, acceptstatus)
        saleStatusFilteredOffers = filterOffers_bySaleStatus(statusFilteredOffers, sale_status)
    else:
        return allOffers #no such address
    #sort list by key
    #compile sorted list and return
    
    return str(passingData)

def getOffers(address):
    import json
    try:
        datadir = '/tmp/msc-webwallet/addr'
        filepath =  datadir + '/' + address + '.json'
        f=open( filepath , 'r' )
        return json.loads(f.readline())
    except IOError:
        return 'no such address'
    
def filterOffers_byCurrency(offers, currencytype):
    #1 is TMSC 
    #0 is MSC
    currency = '1' 
    if currencytype != 'MSC':
        currency = '0'
    del offers[currency]
    return offers

def filterOffers_byType(offers, offertype):
    #accept_tx are offers accepted
    #bought_tx are offers bought
    #offer_tx are offers of sale
    #sold_tx are offers sold
    #recieved and sent tx are simple send
    #exodus tx is not related to offers
    offerstruct = {}
    for key in offers:
        if isinstance(offers[key],dict):
            if offertype == 'BOTH':
                offerstruct['accept_tx'] = offers[key]['accept_transactions']
                offerstruct['bought_tx'] = offers[key]['bought_transactions']
                offerstruct['offer_tx'] = offers[key]['offer_transactions']
                offerstruct['sold_tx'] = offers[key]['sold_transactions']
                return offerstruct
            elif offertype == 'ACCEPT': #accept_tx
                offerstruct['accept_tx'] = offers[key]['accept_transactions']
                offerstruct['bought_tx'] = offers[key]['bought_transactions']
                return offerstruct
            elif offertype == 'SELL': #offer_tx
                offerstruct['offer_tx'] = offers[key]['offer_transactions']
                offerstruct['sold_tx'] = offers[key]['sold_transactions']
                return offerstruct

def filterOffers_byStatus(offers, status):
    #status is the key
    # open closed invalid expired all
    offerstruct = {}
    for transactiontype in offers:
        for tx in offers[transactiontype]:
            print tx
            if tx and status == 'ALL':
                return
            elif status == 'OPEN':
                return
            elif status == 'CLOSED':
                return
            elif status == 'INVALID':
                if tx.invalid.upper() == 'TRUE':
                    offerstruct.push(tx);
                return
            elif status == 'EXPIRED':
                return
def filterOffers_bySaleStatus(one, two):
    return 'implement me'

def offers_handler(environ, start_response):
    return general_handler(environ, start_response, offers_response)
