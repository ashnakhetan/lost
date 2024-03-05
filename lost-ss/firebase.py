import firebase_admin
from firebase_admin import db
import json

cur_city = "Miami"

def connect_db():
    cred_obj = firebase_admin.credentials.Certificate('/Users/ashnakhetan/Desktop/Import/lost-2317d-firebase-adminsdk-8s3gl-deef4eb57f.json')
    default_app = firebase_admin.initialize_app(cred_obj, {
        'databaseURL':'https://lost-2317d-default-rtdb.firebaseio.com/'
        })
    
    # add Destinations object if it doesn't already exist
    ref = db.reference("/")
    if not ref.get() or "Destinations" not in ref.get():
        ref.push().set({
            "Destinations": {}
        })


    # add city if it doesn't already exist
    ref = db.reference("/Destinatons")
    if not ref.get() or cur_city not in ref.get():
        ref.push().set({
            "Destinations":
            {
                cur_city: -1
            }
        })
    
def save_attraction_db(atn_name, img_url):
    ref = db.reference(f"/Destinations/{cur_city}/")
    # Set the image URL in the database if dataset empty or doesn't contain the attraction
    if not ref.get() or atn_name not in ref.get():
        ref.child(atn_name).push().update({
                "image_url": img_url,
                "count": 1
        })
    else: 
        ref.child(atn_name).child("count").set(ref.child(atn_name).child("count").get() + 1)