from rest_framework import viewsets, permissions
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # القائد يرى كل المهام، العضو يرى مهامه فقط
        user = self.request.user
        if user.is_leader:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)