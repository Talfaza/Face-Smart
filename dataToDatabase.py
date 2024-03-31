import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':"https://facesmart1-default-rtdb.europe-west1.firebasedatabase.app/",

})

reference = db.reference('Workers')
data = {
    '0922': {
        'name':"Barake Obama",
        'Job':"President",
        'Tache':"Coding",
        'total_attendence': 10,
        'lastAttendenceDate':"2024-03-31 00:45:15"
    },
    '8685': {
        'name':"Elon Musk",
        'Job':"President",
        'Tache':"Coding",
        'total_attendence': 10,
        'lastAttendenceDate': "2024-03-31 00:45:15"

    }
}

for key, val in data.items():
    reference.child(key).set(val)