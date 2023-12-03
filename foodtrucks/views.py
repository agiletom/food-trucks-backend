from django.http import JsonResponse
from django.core.serializers import serialize
from datetime import datetime
from foodtrucks.models import FoodTruck
import csv
from math import radians, cos, sin, asin, sqrt

def read_csv():
  with open("static/food-truck-data.csv") as file:
    csvreader = csv.reader(file)
    headers = next(csvreader)  # Skip the header row if your CSV file has headers
    trucks = []

    for row in csvreader:
      try:
        # Convert each field to the appropriate data type
        truck_data = {
          'model': 'foodtrucks.FoodTruck',
          'fields': {
            'locationId': int(row[0]),
            'applicant': str(row[1]),
            'facilityType': str(row[2]),
            'cnn': int(row[3]),
            'locationDescription': str(row[4]),
            'address': str(row[5]),
            'blocklot': str(row[6]),
            'block': str(row[7]),
            'lot': str(row[8]),
            'permit': str(row[9]),
            'status': str(row[10]),
            'foodItems': str(row[11]),
            'x': float(row[12]),
            'y': float(row[13]),
            'latitude': float(row[14]),
            'longitude': float(row[15]),
            'schedule': str(row[16]),
            'dayshours': str(row[17]),
            'approved': str(row[19]),
            'received': str(row[20]),
            'priorPermit': bool(int(row[21])),
            'expirationDate': datetime.strptime(row[22], "%m/%d/%Y %I:%M:%S %p").strftime("%Y-%m-%d %H:%M:%S"),
            'location': str(row[23]),
            'firePreventionDistricts': int(row[24]),
            'policeDistricts': int(row[25]),
            'supervisorDistricts': int(row[26]),
            'zipCodes': int(row[27]),
            'neighborhoods': int(row[28]),
          }
        }
        trucks.append(truck_data)
      except ValueError as e:
        print(f"Error processing row {row}: {e}")
      
  return trucks

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