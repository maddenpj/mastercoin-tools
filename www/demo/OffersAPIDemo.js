var initialAmount = 0;
function APITestController($scope, $http) {
    $scope.transactionInformation;
 
    $scope.footer = "FOOTER";
    $scope.title = "TITLE";
    
    var ctype = "tmsc";
    function getAddress() {
       return $('.btcaddress').val();
    }
    
    function makeRequest(offer, valid, accept, sale) {
      //     SELL OFFER OPTIONS     |  ACCEPT OFFER OPTIONS
      // TMSC or MSC                                       
      // SELL or ACCEPT                                    
      // VALID, INVALID, EXPIRED or ANY                    
      // [NONE, SOME, CLOSED, or ANY], [N/A]               
      // [NONE, SOME, CLOSED, or ANY], [WAITING, PAID, N/A]
      var postData = { 
        address: getAddress(), 
        currencyType: ctype,   
        offerType: offer,      
        validityStatus: valid, 
        acceptsStatus: accept, 
        salesStatus: sale      
      };
      console.log("POST DATA: ", postData);
      $.post('/api/offers/', postData , function(data,status,headers,config) {
         $('.dataSection').text(JSON.stringify(data));
         console.log(data);
      });
    }

    //Sell Orders
    $scope.NoAcceptsAndOpen = function() {
      makeRequest('SELL', 'VALID', 'NONE', 'NONE');
    };                                     
    $scope.SomeAcceptsAndOpen = function() {
      makeRequest('SELL', 'VALID', 'SOME', 'NONE');
    };
    $scope.ClosedForAccepts = function() {
      makeRequest('SELL', 'VALID', 'CLOSED', 'NONE');
    };
    $scope.PaidPartiallyAndOpenToAccepts = function() {
      makeRequest('SELL', 'VALID', 'ANY', 'SOME');
    };
    $scope.PaidPartiallyAndClosedToAccepts = function() {
      makeRequest('SELL', 'VALID', 'CLOSED', 'SOME');
    };
    $scope.PaidFullyAndClosed = function() {
      makeRequest('SELL', 'VALID', 'CLOSED', 'CLOSED');
    };
    $scope.SellingCancelled = function() {
      makeRequest('SELL', 'EXPIRED', 'ANY', 'ANY');
    };
    $scope.SellingInvalid = function() {
      makeRequest('SELL', 'INVALID', 'ANY', 'ANY');
    };
    
    
   //Accept Orders
    $scope.AcceptedAwaitingPayment = function() {
      makeRequest('ACCEPT', 'VALID', 'N/A', 'WAITING');
    };
    $scope.AcceptedAndPaid = function() {
      makeRequest('ACCEPT', 'VALID', 'N/A', 'PAID');
    };
    $scope.AcceptedAndExpired = function() {
      makeRequest('ACCEPT', 'EXPIRED', 'N/A', 'N/A');
    };
    $scope.AcceptingInvalid = function() {
      makeRequest('ACCEPT', 'INVALID', 'N/A', 'N/A');
    };
}




$(document).ready(function myfunction() {

    
});


