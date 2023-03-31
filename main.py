import boto3, random, cv2, sys
import numpy as np
from io import BytesIO
from PIL import Image
from smart_open import open

BUCKET: str = 'animals-staying-hydrated'

def select_text() -> str:

    list_of_text = ["Hey You, Stay Hydrated!"]
    return list_of_text[random.randint(0, len(list_of_text) - 1)]


def select_image(s3) -> str:

    bucket = s3.Bucket(BUCKET)

    images: list = []

    for obj in bucket.objects.all():
        object_path = obj.key
        moniker = object_path.split("/")[0]
        if moniker == "images":
            images.append(object_path)

    return images[random.randint(0, len(images) - 1)]

def extract_text(s3, file_name: str) -> str:
    s3_object = s3.Object(BUCKET, file_name)
    print(s3_object.get())

    return "Hey You, Stay Hydrated!"

def png_bytes_to_numpy(png):
    return np.array(Image.open(BytesIO(png)))

def caption_image(s3, file_name: str, text: str) -> int:
    
    s3_object = s3.Object(BUCKET, file_name)
    img = s3_object.get()['Body'].read()
    img  = png_bytes_to_numpy(img)

    org = (50,img.shape[1] - 50)
    fontScale: int = 2

    cv2.putText(img=img, text=text, org=org, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=fontScale, color=(0, 0, 0), thickness=20)
    cv2.putText(img=img, text=text, org=org, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=fontScale, color=(255, 255, 255), thickness=10)

    return img

def main() -> int:

    aws_access_key_id = sys.argv[1]
    aws_secret_access_key = sys.argv[2]

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    s3 = session.resource('s3')

    selected_image = select_image(s3)
    selected_text = select_text()
    
    img = caption_image(s3, selected_image, selected_text)
    
    cv2.imwrite('image.png',img)

    return 0

if __name__ == "__main__":
    main()
