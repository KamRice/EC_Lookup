import json
import sys

from app.services.ec_lookup import find_elevation_certificates

parcel = sys.argv[1] if len(sys.argv) > 1 else input("Parcel number: ")
print(json.dumps(find_elevation_certificates(parcel), indent=2))
#for entry in find_elevation_certificates(parcel):
    #print(entry["documentId"])