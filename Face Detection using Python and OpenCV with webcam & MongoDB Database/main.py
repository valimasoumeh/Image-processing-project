import cv2
import face_recognition
import os
import numpy as np
from db import get_data_base, get_images_from_db, upload_image

db = get_data_base()

names = []

db_images = get_images_from_db(db)

for item in db_images:
    curImage = cv2.imread(db_images)
    db_images.append(curImage)
    names.append(os.path.splitext(item)[0])
# print(images)
print(names)


# endregion

# region Encode Known Images
def find_encodings(images, encode_list):
    encode_list = encode_list
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list


known_encode_list = find_encodings(db_images, encode_list=[])
# print(known_encode_list[0])
print("Encoding Completed!")
# endregion

cap = cv2.VideoCapture(0)

# region Process Frames and compare them with Known Images
while True:
    success, frame = cap.read()
    frame_small = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    fame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
    faces_loc = face_recognition.face_locations(frame_small)
    faces_encode = face_recognition.face_encodings(frame_small, faces_loc)

    for encodeFace, faceLoc in zip(faces_encode, faces_loc):
        matches = face_recognition.compare_faces(known_encode_list, encodeFace)
        face_distances = face_recognition.face_distance(known_encode_list, encodeFace)
        matchIndex = np.argmin(face_distances)

        if matches[matchIndex]:
            name = names[matchIndex].upper()
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (255, 0, 255), cv2.FILLED)
            cv2.putText(frame, name,
                        (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        else:
            person_name = input('i dont know u can tell me your name')
            name_image = f"images/{person_name}.jpg"
            image = cv2.imwrite(name_image, frame)
            upload_image(db, name_image)
            find_encodings(image, known_encode_list)

    cv2.imshow('webcam', frame)
    if cv2.waitKey(1) == ord('q'):
        break
# endregion

cap.release()
os.rmdir('images')
cv2.destroyAllWindows()

