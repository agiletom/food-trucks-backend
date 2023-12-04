from django.http import JsonResponse
from django.core.serializers import serialize
from datetime import datetime
from foodtrucks.models import FoodTruck
import csv
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
  # Convert decimal degrees to radians
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

  # Haversine formula
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a))
  r = 6371  # Radius of earth in kilometers. Use 3956 for miles
  return c * r
        
def trucks(request):
  user_lat = float(request.GET.get('lat', 0))
  user_lng = float(request.GET.get('lng', 0))

  trucks_data = FoodTruck.objects.values('latitude', 'longitude', 'locationDescription')

  # Convert the QuerySet to a list (array)
  trucks_array = list(trucks_data)

  trucks_with_distance = [
    {
      **tr,
      'lat': tr['latitude'],
      'lng': tr['longitude'],
      'distance': haversine(user_lat, user_lng, tr['latitude'], tr['longitude'])
    }
    for tr in trucks_array
  ]

  sorted_trucks = sorted(trucks_with_distance, key=lambda x: x['distance'])

  return JsonResponse(
    { 
      'nearests': sorted_trucks[:5],
      'remains': sorted_trucks[5:] 
    }, 
    safe=False
  )