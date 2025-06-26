from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Feedback(models.Model):
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='given_feedback', null=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_feedback')

    thoughts = models.TextField()
    further_action = models.TextField(null=True, blank=True)

    SENTIMENT_OPTIONS = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]

    sentiment = models.CharField(max_length=10, choices=SENTIMENT_OPTIONS)
    reviewed = models.BooleanField(default=False)
    score = models.PositiveSmallIntegerField(null=True)
    manager_comment = models.TextField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    '''class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(manager = models.F('employee')),
                name='prevent_self_feedback'
            )
        ]'''
    
    def __str__(self):
        return f"{self.employee.username} Feedback (Reviewed: {self.reviewed})"
    

class FeedbackComment(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='comments')
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} commented on {self.feedback.id}"