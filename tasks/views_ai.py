# tasks/views_ai.py
import os
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from .models import Task
from .serializers import TaskSerializer

# Load API key safely
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


class AudioUploadView(APIView):
    """
    API endpoint to handle audio uploads + AI transcription (Whisper).
    """

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()

            if client and task.audio_file:
                try:
                    # Open uploaded file for transcription
                    with open(task.audio_file.path, "rb") as f:
                        transcript = client.audio.transcriptions.create(
                            model="whisper-1",
                            file=f,
                        )

                    # ✅ OpenAI returns `transcript.text` or `transcript["text"]`
                    text = getattr(transcript, "text", None) or transcript.get("text")
                    task.transcript = text.strip() if text else None

                    # 🔹 Title + content logic
                    if task.transcript:
                        # Use first 5 words as title if title missing
                        if not task.title:
                            words = task.transcript.split()[:5]
                            task.title = " ".join(words)
                        # Use full transcript as content if not provided
                        if not task.content:
                            task.content = task.transcript
                    else:
                        # Fallback title
                        fallback_title = (
                            f"Voice Note - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                        )
                        task.title = task.title or fallback_title
                        task.content = task.content or "No transcription available."

                    task.save()

                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
