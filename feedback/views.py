from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feedback, FeedbackComment
from .serializers import FeedbackSerializer, FeedbackCommentSerializer, FeedbackReviewSerializer
from .permissions import IsManager
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from activity.utils import log_activity
import logging


logger = logging.getLogger(__name__)
User = get_user_model()

class FeedbackCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            logger.error(f"error: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        feedback = serializer.save(employee = request.user, manager = request.user.manager_id)
        logger.info(f"feedback: {feedback.id} is posted by {feedback.manager} to {feedback.employee}")
        log_activity(request.user, "Submitted feedback")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FeedbackReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        feedback = Feedback.objects.filter(pk = pk).first()
        if not feedback:
            return Response({"detail" : "Feedback not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FeedbackReviewSerializer(feedback, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(reviewed=True)
        log_activity(request.user, f"Reviewed feedback ID {feedback.id}")
        return Response(FeedbackSerializer(feedback).data, status=status.HTTP_200_OK)
    

class EmployeeFeedbackListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        feedbacks = Feedback.objects.filter(employee=request.user).order_by('-created_at')
        serializer = FeedbackSerializer(feedbacks, many=True)
        logger.info(f"{request.user.username} viewed feedbacks")
        return Response(serializer.data, status=status.HTTP_200_OK)

class ManagerFeedbackListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def get(self, request):
        if not request.user.is_manager:
            raise PermissionDenied("only managers can view feedback history")
        feedbacks = Feedback.objects.filter(manager=request.user, reviewed=False).order_by('-created_at')
        serializer = FeedbackSerializer(feedbacks, many=True)
        logger.info(f"{request.user.username} viewed feedbacks")
        return Response(serializer.data, status=status.HTTP_200_OK)

class FeedbackCommentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FeedbackCommentSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Error: {serializer.errors}")
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        comment = serializer.save(employee = request.user)
        logger.info(f"{comment.employee} commented on feedback {comment.feedback} - comment_id: {comment.id}")
        return Response(serializer.data, status=status.HTTP_200_OK)

class FeedbackCommentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, feedback_id):
        comments = FeedbackComment.objects.filter(feedback_id=feedback_id)
        serializer = FeedbackCommentSerializer(comments, many=True)
        logger.info(f"{request.user.id} viewed comments for feedback: {feedback_id}")
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedbackCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        feedback_count = Feedback.objects.filter(employee=user, manager=user.manager_id).count()

        return Response({
            "feedback_submitted_count": feedback_count
        }, status=status.HTTP_200_OK)


class FeedbackPendingReviewCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_manager:
            return Response({
                "detail" : "Only managers could have access"
            }, status=status.HTTP_401_UNAUTHORIZED)
        feedback_count = Feedback.objects.filter(manager=user, reviewed=False).count()

        return Response({
            "feedback_pending_count": feedback_count
        }, status=status.HTTP_200_OK)

class ReviewedFeedbackListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        feedbacks = Feedback.objects.filter(manager=user, reviewed=True).order_by('-updated_at')
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
