import math

class Coordinate:

   def setLatitude(self, lat):
      self.latitude = lat

   def setLongitude(self, lon):
      self.longitude = lon

   def getLatitude(self):
      return self.latitude
   
   def getLongitude(self):
      return self.longitude

   def getLatitudeRadians(self):
      return math.radians(self.getLatitude())
   
   def getLongitudeRadians(self):
      return math.radians(self.getLongitude())

   def distanceInMeters(self, otherCoord):
      earthRadiusInMeters = 6371000.0
      deltaLat = (otherCoord.getLatitudeRadians() - self.getLatitudeRadians())
      deltaLong = (otherCoord.getLongitudeRadians() - self.getLongitudeRadians())
      
      a = (math.sin(deltaLat / 2) * math.sin(deltaLat / 2) +  
          math.cos(self.getLatitudeRadians()) * math.cos(otherCoord.getLatitudeRadians()) * 
          math.sin(deltaLong / 2) * math.sin(deltaLong / 2))
      c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
      return earthRadiusInMeters * c
