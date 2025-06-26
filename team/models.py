from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Team(models.Model):
    name = models.CharField(max_length=50, null=False)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_teams')
    members = models.ManyToManyField(User, through='TeamMembership', related_name='teams')

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    invited_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee'], name='unique_employee_membership')
        ]
    
    def __str__(self):
        return f"{self.employee.username} in {self.team.name} - {'Accepted' if self.is_accepted else 'Pending'}"