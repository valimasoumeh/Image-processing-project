from pymongo import MongoClient
import gridfs
from bson import Regex


def get_data_base():
    client = MongoClient(
        'mongodb+srv://admin:admin@cluster0.picng.mongodb.net/face?retryWrites=true&w=majority')

    return client['face']


def upload_image(data_base, image_path):
    try:
        fs = gridfs.GridFS(data_base)
        with open(image_path, 'rb') as f:
            contents = f.read()
        fs.put(contents, filename=image_path)

    except Exception as ve:
        print(ve)


def get_images_from_db(data_base):
    try:
        fs = gridfs.GridFS(data_base)
        data = []
        for f in fs.find({'filename': Regex(r'.*\.(png|jpg)')}):
            data.append(f)
        return data
    except Exception as ve:
        print(ve)


if __name__ == "__main__":
    db = get_data_base()
    upload_image(db, '/home/mahdi/bot/1/images/photo_2022-05-10_21-58-11.jpg')
    images = get_images_from_db(db)
