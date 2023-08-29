"""View module for handling requests about businesss"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from businessapi.models import Business, BusinessType, User


class BusinessView(ViewSet):
    """business view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single business
        Returns:
            Response -- JSON serialized business
        """

        try:
            business = Business.objects.get(pk=pk)
            serializer = BusinessSerializer(business)
            return Response(serializer.data)
        except Business.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all businesses
        Returns:
            Response -- JSON serialized list of businesses
        """

        businesses = Business.objects.all()
        business_type = request.query_params.get('type', None)
        if business_type is not None:
            businesses = businesses.filter(business_type_id=business_type)
        serializer = BusinessSerializer(businesses, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized business instance
        """
        user = User.objects.get(uid=request.data["user"])
        business_type = BusinessType.objects.get(
            pk=request.data["business_type"])

        business = Business.objects.create(
            name=request.data["name"],
            pitch=request.data["pitch"],
            area=request.data["area"],
            cost=request.data["cost"],
            business_type=business_type,
            user=user,
        )
        serializer = BusinessSerializer(business)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a business

        Returns:
        Response -- Empty body with 204 status code
        """

        business = Business.objects.get(pk=pk)
        business.name = request.data["name"]
        business.pitch = request.data["pitch"]
        business.area = request.data["area"]
        business.cost = request.data["cost"]

        business_type = BusinessType.objects.get(
            pk=request.data["business_type"])
        business.business_type = business_type
        business.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        business = Business.objects.get(pk=pk)
        business.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class BusinessSerializer(serializers.ModelSerializer):
    """JSON serializer for businesss
    """
    class Meta:
        model = Business
        fields = ('id', "business_type", "name", "pitch", "user",
                  "area", "cost")
        depth = 1
