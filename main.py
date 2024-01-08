import cvzone
import numpy as np
import face_recognition
import cv2
import face_recognition
import os
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
{
    'databaseURL':"https://myprojectml-d0010-default-rtdb.firebaseio.com/",
    'storageBucket':"myprojectml-d0010.appspot.com"
})

cap=cv2.VideoCapture(0)
cap.set(3,480)
cap.set(4,640)
imgbackground=cv2.imread("resources/background.png")
folderModePath='resources/modes'
modePathList=os.listdir(folderModePath)
imgModeList=[]
bucket=storage.bucket()


for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))



file=open("EncodeFile.p",'rb')
encodingsListKnownWithIds=pickle.load(file)
file.close()
encodingsListKnown,studentsIds=encodingsListKnownWithIds

print(studentsIds)
modeType=0
counter=0
id=-1
imgStudent=[]

while True:

     success,img=cap.read()
     imgS=cv2.resize(img,(0,0),None,0.25,0.26)
     imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
     #cv2.namedWindow("output", cv2.WINDOW_NORMAL)
     #cv2.resizeWindow("output", 640, 480)
     faceCurFrame=face_recognition.face_locations(imgS)
     encodedCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)


     imgbackground[162:162+480,55:55+640]=img
     imgbackground[44:44+633,808:808+414]=imgModeList[modeType]

     for encodeFace,faceLoc in zip(encodedCurFrame,faceCurFrame):
         matches=face_recognition.compare_faces(encodeFace,encodingsListKnown)
         faceDis=face_recognition.face_distance(encodeFace,encodingsListKnown)
         # print("matches",matches)
         #print("faceDis",faceDis)
         matchIndex=np.argmin(faceDis)
         if matches[matchIndex]:
             #print("face detected")
             #print(studentsIds[matchIndex])
             y1, x2, y2, x1 = faceLoc
             y1, x2, y2, x1 = 4 * y1, 4 * x2, 4 * y2, 4 * x1
             bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
             imgbackground = cvzone.cornerRect(imgbackground, bbox, rt=0)
             id = studentsIds[matchIndex]


             if counter==0:
                 counter=1
                 modeType=1


     if counter!=0:

         if counter==1:
             studentInfo=db.reference(f'Students/{id}').get()
             print(studentInfo)
             blob=bucket.get_blob(f'images/{id}.png')
             array=np.frombuffer(blob.download_as_string(),np.uint8)
             imgStudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

             datetimeObject=datetime.strptime(studentInfo['last_attendance_time']
                                              ,"%Y-%m-%d %H:%M:%S")
             secondsElapsed=(datetime.now()-datetimeObject).total_seconds()

             if secondsElapsed>10:
                 ref = db.reference(f'Students/{id}')
                 studentInfo['total_attendance'] += 1
                 ref.child('total_attendance').set(studentInfo['total_attendance'])
                 ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

             else:
                 modeType=3
                 counter=0
                 imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


         if 10<counter<20:
             modeType=2


         imgbackground[44:44+633,808:808+414]=imgModeList[modeType]

         if counter<=10 and modeType!=3:

             cv2.putText(imgbackground, str(studentInfo['total_attendance']), (861, 125),
                         cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

             cv2.putText(imgbackground, str(studentInfo['major']), (1006, 550),
                         cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
             cv2.putText(imgbackground, str(id), (1006, 493),
                         cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
             cv2.putText(imgbackground, str(studentInfo['standing']), (910, 625),
                         cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
             cv2.putText(imgbackground, str(studentInfo['year']), (1025, 625),
                         cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
             cv2.putText(imgbackground, str(studentInfo['starting_year']), (1125, 625),
                         cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

             (w, h), _ = cv2.getTextSize(str(studentInfo['name']), cv2.FONT_HERSHEY_COMPLEX,
                                         1, 1)
             offset = (414 - w) // 2
             cv2.putText(imgbackground, str(studentInfo['name']), (offset + 808, 445),
                         cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

             imgbackground[175:175 + 216, 909:909 + 216] = imgStudent
             cv2.waitKey(90)

         counter+=1


         if counter>=20:
             counter=0
             modeType=0
             studentInfo=[]
             imgStudent=[]
             imgbackground[44:44+633,808:808+414]=imgModeList[modeType]


     cv2.imshow("output",imgbackground)
     if cv2.waitKey(1) & 0xFF==ord('q'):
         break