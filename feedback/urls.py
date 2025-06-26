from django.urls import path
from .views import (
    FeedbackCommentCreateView, 
    FeedbackCommentListView, 
    EmployeeFeedbackListView, 
    ManagerFeedbackListView, 
    FeedbackCreateView,
    FeedbackReviewView,
    FeedbackCountView,
    FeedbackPendingReviewCountView,
    ReviewedFeedbackListView
)


urlpatterns = [
    path('create/', FeedbackCreateView.as_view(), name="create_feedback"),
    path('review/<int:pk>/', FeedbackReviewView.as_view(), name="review_feedback"),
    path("view/employee/", EmployeeFeedbackListView.as_view(), name="view_employee_feedback"),
    path("view/", ManagerFeedbackListView.as_view(), name="view_manager_feedback"),
    path("comment/create/", FeedbackCommentCreateView.as_view(), name="create_comment"),
    path("comment/<int:feedback_id>/", FeedbackCommentListView.as_view(), name="view_comment"),
    path("count/", FeedbackCountView.as_view(), name="feedback_count"),
    path("pending/count/", FeedbackPendingReviewCountView.as_view(), name='pending_count'),
    path("reviewed/", ReviewedFeedbackListView.as_view(), name='reviewed_feedbacks'),
]
