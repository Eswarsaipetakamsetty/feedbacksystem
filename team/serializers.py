from rest_framework import serializers
from django.utils import timezone
from .models import Team, TeamMembership
from userauth.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamSerializer(serializers.ModelSerializer):
    manager = serializers.StringRelatedField(read_only=True)
    members = serializers.SerializerMethodField()
    

    class Meta:
        model = Team
        fields = ['id', 'name', 'manager', 'members']
    
    def get_manager(self, obj):
        if obj.manager:
            return {
                "id" : obj.manager.id,
                "username" : obj.manager.username,
                "email" : obj.manager.email,
            }
        return None
    
    def get_members(self, obj):
        request_user = self.context.get("request").user
        is_manager = obj.manager == request_user

        memberships = TeamMembership.objects.filter(team=obj)
        if not is_manager:
            memberships = memberships.filter(is_accepted=True)

        return TeamMembershipSerializer(memberships, many=True).data 
    
    def create(self, validated_data):
        members = validated_data.pop('members', [])
        team = Team.objects.create(manager=self.context["request"].user, **validated_data)
        for member in members:
            TeamMembership.objects.create(team=team, employee=member)
        return team
    
    def validate_member_ids(self, members):
        already_in_team = TeamMembership.objects.filter(employee__in=members).values_list('employee_id', flat=True)
        if already_in_team:
            usernames = User.objects.filter(id__in=already_in_team).values_list('username', flat=True)
            raise serializers.ValidationError(f"These users already belong to a team: {', '.join(usernames)}")
        return members
    
class TeamMembershipSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    employee_details = UserSerializer(source='employee', read_only=True)
    class Meta:
        model = TeamMembership
        fields = ["id", "team", "employee", "is_accepted", "invited_at", "accepted_at", "employee_details"]
        read_only_fields = ["invited_at", "accepted_at", "is_accepted"]
