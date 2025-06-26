from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Activity
from .serializers import ActivitySerializer

class ActivityListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        activities = Activity.objects.filter(user=request.user).order_by('-timestamp')[:5]
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
