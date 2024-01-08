import cv2
import face_recognition
import os
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
{
    'databaseURL':"https://myprojectml-d0010-default-rtdb.firebaseio.com/",
    'storageBucket':"myprojectml-d0010.appspot.com"
})


folderModePath='images'
PathList=os.listdir(folderModePath)
imgList=[]
studentsIds=[]
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderModePath,path)))
    studentsIds.append(os.path.splitext(path)[0])
    fileName=f'{folderModePath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)


print(studentsIds)
def findEncodings(imgList):
    encodeList=[]
    for img in imgList:
        cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodingsListKnown=findEncodings(imgList)
encodingsListKnownWithIds=[encodingsListKnown,studentsIds]
file=open("EncodeFile.p",'wb')
pickle.dump(encodingsListKnownWithIds,file)
file.close()