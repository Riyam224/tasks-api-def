# tasks/views_ai.py
import os
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from .models import Task
from .serializers import TaskSerializer

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


class AudioUploadView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()

            if task.audio_file:
                try:
                    with open(task.audio_file.path, "rb") as f:
                        transcript = client.audio.transcriptions.create(
                            model="whisper-1", file=f
                        )

                    task.transcript = (
                        transcript.text.strip() if transcript.text else None
                    )

                    # 🔹 Fallback title logic
                    if task.transcript:
                        # Use first 5 words
                        words = task.transcript.split()[:5]
                        task.title = " ".join(words)
                        # Use full transcript as content if not provided
                        if not task.content:
                            task.content = task.transcript
                    else:
                        # If no transcript, fallback to date-based title
                        fallback_title = (
                            f"Voice Note - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                        )
                        task.title = fallback_title
                        if not task.content:
                            task.content = "No transcription available."

                    task.save()

                except Exception as e:
                    return Response({"error": str(e)}, status=500)

            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
