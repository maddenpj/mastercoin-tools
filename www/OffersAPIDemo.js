var initialAmount = 0;
function APITestController($scope, $http) {
    $scope.transactionInformation;
 
    $scope.footer = "FOOTER";
    $scope.title = "TITLE";

    $scope.NoAcceptsAndOpen = function() {
      $.post('/api/offers/', { addr: $('.btcaddress').val(),currencytype: "tmsc", offertype: 'sell', status: 'open', salestatus:'no_accepts' },function(data,status,headers,config) {
         $('.dataSection').text(JSON.stringify(data));
         console.log(data);
      });
    }
   /*
    $scope.NoAcceptsAndOpen = function() {}
    $scope.NoAcceptsAndOpen = function() {}
    $scope.NoAcceptsAndOpen = function() {}
    $scope.NoAcceptsAndOpen = function() {}
    $scope.NoAcceptsAndOpen = function() {}
    $scope.NoAcceptsAndOpen = function() {}
    $scope.NoAcceptsAndOpen = function() {}
    */
    
    $scope.getSellofferData = function () {

        // parse tx from url parameters
        var myURLParams = BTCUtils.getQueryStringArgs();
        var file = 'tx/' + myURLParams['tx'] + '.json';

        // Make the http request and process the result

        $http.get(file, {}).success(function (data, status, headers, config) {
            $scope.transactionInformation = data[0];

            $scope.transactionInformation.formatted_amount = parseFloat($scope.transactionInformation.formatted_amount);
            initialAmount = $scope.transactionInformation.formatted_amount;

            $scope.transactionInformation.to_address = 11;
            //Create step for input type number
            var amount = $scope.transactionInformation.formatted_amount.toString();
            //Whole number
            if (amount.indexOf(".") == -1) {
                console.log('Whole number');
                $scope.step = "1";
            }
            else {//Decimal number
                var decimalN = amount.substr(amount.indexOf(".") + 1);
                var step = "0.";
                for (var i = 0; i < decimalN.length - 1; i++) {
                    step += "0";
                }
                step += "1";
                $scope.step = step;
            }
        });
      
    }

}




$(document).ready(function myfunction() {

    
});


