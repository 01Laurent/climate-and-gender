import folium
from folium import plugins
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import render

from .models import HealthFacilities


def map_view(request):
    m = folium.Map(
            location=[0.0, 37.0],
            zoom_start=6
            )

    health_facilities = HealthFacilities.objects.all()

    for facility in health_facilities:
        print(f"Facility: {facility.name}, Location:\
                ({facility.geom.y}, {facility.geom.x})")
        folium.Marker(
                location=[facility.geom.y, facility.geom.x],
                popup="H"
                ).add_to(m)

    map_html = m._repr_html_()

    return render(request, 'map.html', {'map_html': map_html})


def search_health_facilities(request):
    geolocator = Nominatim(user_agent="health_facility")
    query = request.GET.get('query', '')
    area = request.GET.get('area', '')
    user_location = None

    if area:
        location = geolocator.geocode(area)
        if location:
            user_location = Point(
                    location.longitude,
                    location.latitude,
                    srid=4326
                    )
    
    health_facilities = []
    map_object = None

    if user_location:
        health_facilities = HealthFacility.objects.filter(
                name__icontains=query
                ).annotate(distance=Distance(
                    'location',
                    user_location
                    )).order_by('distance')[:10]

        map_object = folium.Map(
                        location=[location.latitude, location.longitude],
                        zoom_start=13
                        )

        folium.Marker(
                [location.latitude, location.longitude],
                popup="Your location",
                icon=folium.Icon(color='blue')
                ).add_to(map_object)

        for facility in health_facilities:
            folium.Marker(
                [facility.location.y, facility.location.x],
                popup=f"<b>{facility.name}</b>\
                        <br>{facility.address}<br>\
                        {facility.services_offered}",
                icon=folium.Icon(color='red')
            ).add_to(map_object)

        map_object = map_object._repr_html_()

    context = {
        'health_facilities': health_facilities,
        'map_object': map_object,
        'area': area,
        'query': query,
    }
    return render(request, 'map.html', context)
