from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, SignupSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsManager
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class EmployeeListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        team_members = self.request.user.team.all()
        serializer_class = UserSerializer(team_members, many=True)
        return Response(serializer_class.data)

    
class SignupView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Signup failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        logger.info(f"User created: {user.email}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetUserByEmailView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({"detail": "Email is required as query param."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class GetUserByIdView(APIView):

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)