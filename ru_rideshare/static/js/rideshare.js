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
