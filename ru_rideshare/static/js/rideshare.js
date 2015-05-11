/* Google Maps API Interaction */

var map = null;
var geocoder = null;
var directionsDisplay = null;
var directionsService = new google.maps.DirectionsService();
markers = [null, null];

function initialize() {
        var mapOptions = {
            center: { lat: 40.498818, lng: -74.441862},
            zoom: 12
        };
        map = new google.maps.Map(document.getElementById('map-canvas'),
                mapOptions);
    geocoder = new google.maps.Geocoder();
    directionsDisplay = new google.maps.DirectionsRenderer();
    directionsDisplay.setMap(map);
}

function showAddress(address, ind, callback) {
  if (!callback) {
    callback = function(){};
  }
  if (geocoder) {
    geocoder.geocode(
      {address: address},
      function(points) {
        if (!points) {
          alert(address + " not found");
        } else {
          latlng = {lat: points[0].geometry.location.lat(), lng: points[0].geometry.location.lng()}
          map.setCenter(latlng, 12);
          markers[ind] = new google.maps.Marker({
              position: latlng,
              map: map,
              title: address,
              animation: google.maps.Animation.DROP,
              draggable: true
          });
        }
        callback();
      }
    );
  }
}

function validateViewForm(formdata, callback) {
    if(formdata["pickup"] != "") {
        if(geocoder) {
            geocoder.geocode(
                {address : formdata["pickup"]},
                function(points) {
                    if(!points) {
                        alert(address + " not found");
                        return;
                    }
                    platlng = {lat: points[0].geometry.location.lat(), lng: points[0].geometry.location.lng()}
                    formdata["plat"] = platlng["lat"];
                    formdata["plon"] = platlng["lng"];
                    if(formdata["dest"] != "") {
                        geocoder.geocode(
                            {address: formdata["dest"]},
                            function(dpoints) {
                                if(!points) {
                                    alert(address + " not found");
                                    return;
                                }
                                dlatlng = {lat: dpoints[0].geometry.location.lat(), lng: dpoints[0].geometry.location.lng()}
                                formdata["dlat"] = dlatlng["lat"];
                                formdata["dlon"] = dlatlng["lng"];
                                callback(formdata);
                            });
                    } else {
                        callback(formdata);
                    }
                });
        }
    } else {
        callback(formdata);
    }
}

function buildRideFromJson(r, callback) {
    if(geocoder) {
        geocoder.geocode(
            { location: {lat: r["dest_lat"], lng: r["dest_long"]} },
            function(dpoints){
                if(!dpoints) return;
                console.log(dpoints);
                geocoder.geocode(
                    { location: {lat: r["pickup_lat"], lng: r["pickup_long"]} },
                    function(ppoints) {
                        if(!ppoints) return;
                        daddr = dpoints[0].formatted_address;
                        paddr = ppoints[0].formatted_address;
                        var outer = "<div id='" + r["id"] + "' class='req link-info'>";
                        var topr = "<p>" + r["rnetid"] + " - " + r["dtime"] + "</p>";
                        var p = "<p id='pickuploc'>Pickup Location: " + paddr + "</p>";
                        var d = "<p id='destloc'>Destination Location: " + daddr + "</p>";
                        var sel = "<input class='req-sel btn btn-default' value='Select This Request'>";
                        callback(outer + topr + p + d + sel + "</div>");
                    });
            });
    }
}

function calcRoute(start, end) {
    var request = {
        origin:start,
        destination:end,
        travelMode: google.maps.TravelMode.DRIVING
    };
    directionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        }
    });
}
