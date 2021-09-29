from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ShortenerSerializer
from urlshortener.models import Shortener
from rest_framework import status
from rest_framework import permissions
from django.http import HttpResponseRedirect


class UrlshortenerListView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        List all the url items for given requested user
        """
        urls = Shortener.objects.filter(user=request.user.id)
        serializer = ShortenerSerializer(urls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create the Url with given url data
        """
        data = {"long_url": request.data.get("url"), "user": request.user.id}
        serializer = ShortenerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UrlshortenerDetailView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, url_id, user_id):
        """
        Helper method to get the object with given url_id, and user_id
        """
        try:
            return Shortener.objects.get(id=url_id, user=user_id)
        except Shortener.DoesNotExist:
            return None

    def get(self, request, url_id, *args, **kwargs):
        """
        Retrieves the Url with given url_id
        """
        url_instance = self.get_object(url_id, request.user.id)
        if not url_instance:
            return Response(
                {"detail": "Object with url id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ShortenerSerializer(url_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, url_id, *args, **kwargs):
        """
        Deletes the url item with given url_id if exists
        """
        url_instance = self.get_object(url_id, request.user.id)
        if not url_instance:
            return Response(
                {"detail": "Object with url id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        url_instance.delete()
        return Response(
            {"detail": "Object deleted!"}, status=status.HTTP_200_OK
        )


class RedirectorView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, short_url, user_id):
        """
        Helper method to get the object with given short_url, and user_id
        """
        try:
            return Shortener.objects.get(short_url=short_url, user=user_id)
        except Shortener.DoesNotExist:
            return None

    def get(self, request, short_url, *args, **kwargs):
        """
        Retrieves the Url with given url_id
        """
        obj = self.get_object(short_url, request.user.id)
        if not obj:
            return Response(
                {"detail": "Object with short_url does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return HttpResponseRedirect(redirect_to=obj.long_url)
