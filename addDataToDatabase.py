import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
{'databaseURL':"https://myprojectml-d0010-default-rtdb.firebaseio.com/"})

ref = db.reference('Students')
data = {
    "1616":
        {
            "name": "Aryan",
            "major": "Mining",
            "starting_year": 2017,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-07-27 00:54:34"
        },
    "1617":
         {
            "name": "Rahulpreet",
            "major": "Mining",
            "starting_year": 2017,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-07-27 00:54:34"
        },
"1618":
         {
            "name": "sayam",
            "major": "Mining",
            "starting_year": 2017,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-07-27 00:54:34"
        },
"1619":
         {
            "name": "gian",
            "major": "Mining",
            "starting_year": 2017,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-07-27 00:54:34"
        },


    "1467":
         {
            "name": "lappu singh",
            "major": "Electronics",
            "starting_year": 2017,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-07-27 00:54:34"
        },
"1620":
         {
            "name": "aadimaanav",
            "major": "Mining",
            "starting_year": 2017,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-07-27 00:54:34"
        },
"1621":
         {
            "name": "tanishq",
            "major": "software",
            "starting_year": 1945,
            "total_attendance": 3,
            "standing": "G",
            "year": 6,
            "last_attendance_time": "2023-07-27 00:54:34"
        }


}

for key,value in data.items():
    ref.child(key).set(value)
