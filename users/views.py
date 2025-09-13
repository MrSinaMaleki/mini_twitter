from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Follow
from .serializers import RegisterSerializer, FollowSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny, ]

# add soft delete
class ToggleFollowView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, user_id):
        target_user = generics.get_object_or_404(User, id=user_id)
        if target_user == request.user:
            return Response({'detail': 'you cannot follow your self.'}, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.filter(follower=request.user, following=target_user).first()

        if follow:
            follow.delete()
            return Response({"detail": f"You unfollowed {target_user.username}"}, status=status.HTTP_200_OK)

        else:
            new_follow = Follow.objects.create(follower=request.user, following=target_user)
            return Response({"detail": f"You followed {target_user.username}"}, status=status.HTTP_201_CREATED)
