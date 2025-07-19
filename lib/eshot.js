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
            var item = bus.HatNumarasi;
            return seen.hasOwnProperty(item) ? false : (seen[item] = true);
        });
    }

    function cleanUpBusData(data) {
        data.forEach(bus => {
            bus.lat = bus.KoorX.replace(',', '.');
            bus.lon = bus.KoorY.replace(',', '.');
            delete bus.KoorX;
            delete bus.KoorY;
        });
        data = data.filter(bus => bus.KalanDurakSayisi < 11);
        data = uniqBus(data);
        return data;
    }

    function getLocation(success, error) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(success, error);
        }
    }

    function readTextFile(file, callback) {
        var rawFile = new XMLHttpRequest();
        rawFile.overrideMimeType("application/json");
        rawFile.open("GET", file, true);
        rawFile.onreadystatechange = function() {
            if (rawFile.readyState === 4 && rawFile.status == "200") {
                callback(rawFile.responseText);
            }
        }
        rawFile.send(null);
    }
    
    function findNearestStops(data, pos) {
        var stops = []
        for (var i=0; i<data.length; i++){
            stop = data[i]
            if (Math.abs(parseFloat(stop.ENLEM) - pos.latitude) < 0.005 
            && Math.abs(parseFloat(stop.BOYLAM) - pos.longitude) < 0.005) {
                stops.push(stop)
            }
        }
        return stops;
    }

    readTextFile("lib/stops.json", function(text){
        var data = JSON.parse(text);
        getLocation( (pos) => {
            console.log(pos)
            var stops = findNearestStops(data, pos.coords)
            console.log(stops)
        }, (err) => {
            console.log(err)
        })
    });

    return {
        getBusLocationsForStop
    }
})();

