from django.shortcuts import render
from rest_framework import status

from .models import Contact
from .serializers import ContactSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class ContactAPIView(APIView):
    serializer_class = ContactSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # if serializer.is_valid():
        #     serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
