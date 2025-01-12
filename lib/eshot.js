var EshotService = (function(){
    
    function getBusLocationsForStop(stopId, onSuccess, onError) {
        if (stopId == '') return;
        fetch('https://openapi.izmir.bel.tr/api/iztek/duragayaklasanotobusler/' + stopId)
            .then(response => response.json())
            .then(data => cleanUpBusData(data))
            .then(data => onSuccess(data))
            .catch((e) => onError(e));
    }
    
    function uniqBus(data) {
        var seen = {};
        return data.filter(function(bus) {
            var item = bus.HatNumarasi+"|"+bus.KalanDurakSayisi;
            return seen.hasOwnProperty(item) ? false : (seen[item] = true);
        });
    }

    var cleanUpBusData = function(data) {
        data.forEach(bus => {
            bus.lat = bus.KoorX.replace(',', '.');
            bus.lon = bus.KoorY.replace(',', '.');
            delete bus.KoorX;
            delete bus.KoorY;
        });
        data = data.filter(bus => bus.KalanDurakSayisi < 10);
        data = uniqBus(data);
        return data;
    }

    return {
        getBusLocationsForStop
    }
})();

