from django.urls import path
from .views import CreateTeamView, TeamListView, AcceptInvitationView, AddTeamMembersView, ManagerTeamsView, TeamCountSummaryView

urlpatterns = [
    path('create/', CreateTeamView.as_view(), name='create_team'),
    path('viewteam/', TeamListView.as_view(), name='view_team'),
    path('accept/<int:team_id>/', AcceptInvitationView.as_view(), name='accept_invitation'),
    path('add_members/<int:team_id>/', AddTeamMembersView.as_view(), name='add_members'),
    path('manager-teams/', ManagerTeamsView.as_view(), name='manager-teams'),
    path('count/', TeamCountSummaryView.as_view(), name='team_count_summary'),
]
