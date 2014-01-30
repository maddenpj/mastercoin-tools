import urlparse
import os, sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
from msc_utils_offerparsing import *
from msc_apps import *
import tempfile

def offers_response(response_dict):
    expected_fields=['addr','currencytype','offertype','status','salestatus']
    for field in expected_fields:
        if not response_dict.has_key(field):
            return (None, 'No field '+field+' in response dict '+str(response_dict))
        if len(response_dict[field]) != 1:
            return (None, 'Multiple values for field '+field)
            
    addr = response_dict['addr']
    curr = response_dict['currencytype'].upper()
    ot = response_dict['offertype'].upper()
    status = response_dict['status'].upper()
    ss = response_dict['salestatus'].upper()
    data = sortdata(addr, curr, ot, status, ss)    
    
    response_status='OK'
    response='{"status":"'+response_status+'", "data":"'+ data +'"}'
    return (response, None)

def sortdata(address,currencytype, offertype, status, sale_status):
    #currencytype = TMSC, MSC
    #offertype = Accept, Sell, Both
    #status = Open, Closed, Invalid, Expired, All
    #sale_status = Accepted/Not Accepted, Paid/Not Paid, All
    
    print address, offertype, status, sale_status
    #get list of all offers by address
    allOffers = getOffers(address)
    if allOffers != 'no such address':
        currencyFilteredOffers = filterOffers_byCurrency(allOffers, currencytype)
        typeFilteredOffers = filterOffers_byType(currencyFilteredOffers, offertype)
        statusFilteredOffers = filterOffers_byStatus(typeFilteredOffers, status)
        saleStatusFilteredOffers = filterOffers_bySaleStatus(statusFilteredOffers, sale_status)
    else:
        return allOffers #no such address
    #sort list by key
    #compile sorted list and return
    
    return saleStatusFilteredOffers

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
            if tx.status.upper() == status == 'ALL':
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
def filterOffers_bySaleStatus():
    return

def offers_handler(environ, start_response):
    return general_handler(environ, start_response, offers_response)
