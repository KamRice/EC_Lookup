from app.config import settings
from app.services.accela_client import get_parcel_records, get_record_documents


def normalize_parcel(parcel_number: str) -> str:
    # Placeholder: adjust once you know how GIS formats parcel IDs
    return parcel_number.strip()


def is_final_ec(doc: dict) -> bool:
    category = ((doc.get("category") or {}).get("value") or "").strip().lower()

    if category != settings.ec_category:
        return False
    else:
        '''
        print("|---MATCHING CATEGORY---|")
        print("Category: ", category, " : ", settings.ec_category)
        '''
    return True


def find_elevation_certificates(parcel_number: str) -> list:
    parcel = normalize_parcel(parcel_number)
    records = get_parcel_records(parcel, settings.record_types)

    found = []
    for rec in records:
        for doc in get_record_documents(rec["id"]):
            if is_final_ec(doc):
                found.append({
                    "recordId": rec["id"],
                    "permit": rec.get("customId"),
                    "documentId": doc.get("id"),
                    "fileName": doc.get("fileName"),
                    "uploaded": doc.get("uploadedDate"),
                })
    return found
