from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Team, TeamMembership
from activity.utils import log_activity
from .serializers import TeamSerializer, TeamMembershipSerializer


User = get_user_model()


class CreateTeamView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not request.user.is_manager:
            return Response({"detail": "Only managers can create team"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        member_emails = data.pop("member_emails", [])

        if not isinstance(member_emails, list) or not all(isinstance(email, str) for email in member_emails):
            return Response({"detail": "member_emails must be a list of valid email strings."},
                            status=status.HTTP_400_BAD_REQUEST)

        members = User.objects.filter(email__in=member_emails)
        found_emails = set(members.values_list("email", flat=True))
        missing_emails = list(set(member_emails) - found_emails)

        if missing_emails:
            return Response({"detail": f"Users not found for emails: {', '.join(missing_emails)}"},
                            status=status.HTTP_404_NOT_FOUND)

        already_in_team = TeamMembership.objects.filter(employee__in=members).values_list('employee__email', flat=True)
        if already_in_team:
            return Response({"detail": f"These users already belong to a team: {', '.join(already_in_team)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        team = Team.objects.create(name=data.get("name"), manager=request.user)
        for user in members:
            TeamMembership.objects.create(team=team, employee=user)
        log_activity(request.user, f"Created {team.name} with members: {member_emails}")
        return Response(TeamSerializer(team, context={"request": request}).data,
                        status=status.HTTP_201_CREATED)
    
class TeamListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        is_manager = False
        teams = Team.objects.filter(manager=request.user).first()
        if teams:
            is_manager = True
        else:
            membership = TeamMembership.objects.select_related('team').filter(employee=request.user).first()
            if membership:
                teams = membership.team
        if not teams:
            return Response({"detail" : "You are not part of any team"}, status=status.HTTP_200_OK)
        context = {'request' : request}
        context['is_manager'] = is_manager

        serializer = TeamSerializer(teams, context = context)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AcceptInvitationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, team_id):
        try:
            membership = TeamMembership.objects.get(team_id=team_id, employee=request.user)
        except TeamMembership.DoesNotExist:
            return Response({"detail": "Membership not found."}, status=status.HTTP_404_NOT_FOUND)

        if membership.is_accepted:
            return Response({"detail": "Invitation already accepted."}, status=status.HTTP_400_BAD_REQUEST)
        
        membership.is_accepted = True
        membership.accepted_at = timezone.now()
        membership.save()

        request.user.manager_id = membership.team.manager
        request.user.save(update_fields=["manager_id"])
        log_activity(request.user, f"Accepted invitation from {membership.team.manager}")
        return Response(TeamMembershipSerializer(membership).data, status=status.HTTP_200_OK)

class AddTeamMembersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)

        if team.manager != request.user:
            raise PermissionDenied("Only the team manager can add members.")

        emails = request.data.get("members", [])

        if not isinstance(emails, list) or not emails:
            raise ValidationError({"members": "Provide a non-empty list of email addresses."})
        
        users = User.objects.filter(email__in=emails)

        if len(users) != len(emails):
            found_emails = set(user.email for user in users)
            missing = set(emails) - found_emails
            return Response(
                {"detail": f"These email(s) were not found: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        already_in_team = TeamMembership.objects.filter(employee__in=users).values_list('employee__email', flat=True)

        if already_in_team:
            return Response({
                "detail": f"Some users already belong to teams: {', '.join(already_in_team)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        added_members = []
        for user in users:
            membership = TeamMembership.objects.create(team=team, employee=user)
            added_members.append(TeamMembershipSerializer(membership).data)
        log_activity(request.user, f"Added {added_members} into team: {team_id}")
        return Response({
            "team": team.id,
            "added_members": added_members
        }, status=status.HTTP_201_CREATED)
    
class ManagerTeamsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.is_manager:
            return Response({"detail": "Only managers can view their teams."}, status=status.HTTP_403_FORBIDDEN)

        teams = Team.objects.filter(manager=user).values('id', 'name')
        return Response(teams, status=status.HTTP_200_OK)

class TeamCountSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        manager_teams = Team.objects.filter(manager=user)

        member_teams = TeamMembership.objects.select_related('team').filter(employee=user).values_list('team', flat=True)
        member_teams_qs = Team.objects.filter(id__in=member_teams)

        all_teams = manager_teams.union(member_teams_qs)

        result = []
        for team in all_teams:
            accepted_count = TeamMembership.objects.filter(team=team, is_accepted=True).count()

            if team.manager == user:
                total_count = accepted_count + 1
            else:
                total_count = accepted_count + 1

            result.append({
                "team_id": team.id,
                "team_name": team.name,
                "total_accepted_members": total_count
            })

        return Response({
            "total_teams": all_teams.count(),
            "teams": result
        }, status=status.HTTP_200_OK)