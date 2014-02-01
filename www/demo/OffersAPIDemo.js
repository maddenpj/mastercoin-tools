var initialAmount = 0;
function APITestController($scope, $http) {
    $scope.transactionInformation;
 
    $scope.footer = "FOOTER";
    $scope.title = "TITLE";
    
    var ctype = "tmsc";
    function getAddress() {
       return $('.btcaddress').val();
    }
    
    function makeRequest(offer, valid,  div) {
      //     SELL OFFER OPTIONS     |  ACCEPT OFFER OPTIONS
      // TMSC or MSC                                       
      // SELL, ACCEPT or BOTH                                    
      var postData = { 
        address: getAddress(), 
        currencyType: ctype,   
        offerType: offer      
      };
      div ? div = $('.dataSection') : div = $('.dataSection2');
      console.log("POST DATA: ", postData);
      $.post('/api/offers/', postData , function(data,status,headers,config) {
         div.text(JSON.stringify(data));
         console.log(data);
      });
    }

    $scope.ShowSellAndPaidOffers = function() {
      makeRequest('SELL', 'VALID', 'NONE', 'NONE', 1);
    };                         
    $scope.ShowAcceptAndBoughtOffers = function() {
      makeRequest('ACCEPT', 'VALID', 'NONE', 'NONE', 1);
    };                                     

}




$(document).ready(function myfunction() {

    
});


