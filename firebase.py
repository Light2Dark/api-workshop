import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('api-workshop-sunway.json')

app = firebase_admin.initialize_app(credential=cred)
db = firestore.client()

doc_ref = db.collection(u'users').document("julio ceasar")
doc_ref.set({
    "first": "Julio",
    "last": "Ceasar"
})