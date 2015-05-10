/* Google Maps API Interaction */

var map = null;
var geocoder = null;
markers = [null, null];

function initialize() {
        var mapOptions = {
            center: { lat: 40.498818, lng: -74.441862},
            zoom: 12
        };
        map = new google.maps.Map(document.getElementById('map-canvas'),
                mapOptions);
    geocoder = new google.maps.Geocoder();
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
            console.log(formdata);
            geocoder.geocode(
                {address : formdata["pickup"]},
                function(points) {
                    if(!points) {
                        alert(address + " not found");
                        return;
                    }
                    platlng = {lat: points[0].geometry.location.lat(), lng: points[0].geometry.location.lng()}
                    console.log("Got lat long");
                    formdata["platlng"] = platlng;
                    delete formdata["pickup"];
                    if(formdata["dest"] != "") {
                        geocoder.geocode(
                            {address: formdata["dest"]},
                            function(dpoints) {
                                if(!points) {
                                    alert(address + " not found");
                                    return;
                                }
                                dlatlng = {lat: dpoints[0].geometry.location.lat(), lng: dpoints[0].geometry.location.lng()}
                                formdata["dlatlng"] = dlatlng;
                                delete formdata["dest"];
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

function buildRideFromJson(r) {
    var outer = "<div id='" + r["id"] + "' class='link-info'>";
    var topr = "<p>" + r["netid"] + " - " + r["time"] + "</p>";
    var p = "<p>Pickup Location: " + r["paddr"] + "</p>";
    var d = "<p>Destination Location: " + r["daddr"] + "</p>";
    var sel = "<input class='req-sel btn btn-default' value='Select This Request'>";
    return outer + topr + p + d + sel + "</div>";
}
