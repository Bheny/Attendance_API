import base64
import io
import cv2
import numpy as np
import face_recognition
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .database import DATABASE_FILES
from django.conf import settings


@api_view(["POST"])
def recognize_faces(request):
    try:
        base64_image_data = request.data.get("video_feed")
        if base64_image_data:
            # Decode base64 image data
            decoded_image_data = base64.b64decode(base64_image_data.split(",")[1])

            # Convert to OpenCV format
            nparr = np.frombuffer(decoded_image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            recognized_faces = []

            for user in DATABASE_FILES:
                # Load known face image and encoding
                known_image = face_recognition.load_image_file(
                    settings.BASE_DIR / user["img"]
                )
                known_face_encoding = face_recognition.face_encodings(known_image)[0]

                # Process video frame to perform face recognition
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(frame_rgb)

                for face_location in face_locations:
                    top, right, bottom, left = face_location
                    face_encoding = face_recognition.face_encodings(
                        frame_rgb, [face_location]
                    )[0]
                    distance = face_recognition.face_distance(
                        [known_face_encoding], face_encoding
                    )[0]

                    if distance < 0.45:
                        recognized_faces.append(
                            [user["id"], base64_image_data, "Present"]
                        )
                    else:
                        recognized_faces.append([user["id"], None, "Absent"])

            return JsonResponse({"recognized_faces": recognized_faces})
        else:
            return JsonResponse(
                {"error": "No video_feed data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
