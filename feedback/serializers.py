from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Feedback, FeedbackComment

User = get_user_model()

class FeedbackSerializer(serializers.ModelSerializer):
    manager = serializers.StringRelatedField(read_only=True)
    employee = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id', 'manager', 'employee', 'thoughts', 'further_action',
            'sentiment', 'reviewed', 'score', 'manager_comment',
            'created_at', 'updated_at'
            ]
        read_only_fields = ['reviewed', 'score', 'manager_comment', 'created_at', 'updated_at']


    '''def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user != attrs.get('employee') and not request.user.is_manager:
            raise serializers.ValidationError("You can give only give feedback to yourself or must be a manager")
        return attrs'''

class FeedbackReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['score', 'manager_comment', 'reviewed']
    
    def validate(self, data):
        if not self.instance:
            raise serializers.ValidationError("Invalid feedback instance.")
        return data
    

class FeedbackCommentSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FeedbackComment
        fields = ['id', 'feedback', 'employee', 'comment', 'created_at']
        read_only_fields = ['created_at']