from django.db.models import Avg, Count, Max, Min
from django.forms import model_to_dict
from django.http import JsonResponse, Http404
from rest_framework.views import APIView

from .models import Dress
from .models import ShowEvent
from .serializers import DressSerializer, RedCarpetSerializer, ShowSerializerList, BrandSerializer2, DressSerializer2, \
    ShowEventSerializerDetail, BrandDressSerializer
from .serializers import BrandSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Brand
from .models import RedCarpetPresentation

@api_view(['GET', 'POST'])
def dress_list(request):

    #get all the dresses
    #serialize them
    #return json
    if request.method == 'GET':
        dresses = Dress.objects.all()
        serializer = DressSerializer(dresses, many=True)
        return Response({"dresses": serializer.data})

    if request.method == 'POST':
        serializer = DressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response("a dress cant be under 89 euros!", status=status.HTTP_400_BAD_REQUEST)



#response is used to return or json or html

@api_view(['PUT', 'DELETE'])
def dress_detail(request, id):

    try:
        dress = Dress.objects.get(pk=id)
    except Dress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DressSerializer(dress)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DressSerializer(dress, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        dress.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def brand_list(request):

    #get all the dresses
    #serialize them
    #return json
    if request.method == 'GET':
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response({"brands": serializer.data})

    if request.method == 'POST':
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response("the number of models must be positive!", status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def brand_detail(request, id):

    try:
        brand = Brand.objects.get(pk=id)
        #dress = Dress.objects.get(pk=id)
    except Brand.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BrandSerializer2(brand)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = BrandSerializer(brand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def filter_brands(request, nr_models):

    if request.method=='GET':
        brands_list=[]
        brands = Brand.objects.all()
        for brand in brands:
            my_model_instance = Brand.objects.get(id=brand.id)
            my_field_value = my_model_instance.nr_models
            if my_field_value > nr_models:
               brands_list.append(brand)
        serializer = BrandSerializer(brands_list, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def nouu(request, id):
    try:
        brand = Brand.objects.get(pk=id)
    except Brand.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BrandSerializer2(brand)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def redcarpetpres_list(request):

    if request.method == 'GET':
        shows = RedCarpetPresentation.objects.all()
        serializer = RedCarpetSerializer(shows, many=True)
        return Response({"red carpet prezenations": serializer.data})

    if request.method == 'POST':
        serializer = RedCarpetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response("the number of guests cannot be negative!", status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def redcarpetpres_detail(request, id):

    try:
        red = RedCarpetPresentation.objects.get(pk=id)
    except Dress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RedCarpetSerializer(red)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RedCarpetSerializer(red, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        red.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def show_event_list(request):

    if request.method == 'GET':
        shows = ShowEvent.objects.all()
        serializer = ShowSerializerList(shows, many=True)
        return Response({"shows": serializer.data})

    if request.method == 'POST':
        serializer = ShowSerializerList(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def show_event_detail(request, id):

    try:
        show = ShowEvent.objects.get(pk=id)
    except ShowEvent.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ShowSerializerList(show)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ShowSerializerList(show, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        show.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# all brands in the order of their dresses prices
class ReportModels(generics.ListCreateAPIView):
    serializer_class = DressSerializer

    def get_queryset(self):
        queryset = Dress.objects.annotate(average_models=Avg('brand_id__nr_models')).order_by('average_models')
        return queryset


class FilterModels(generics.ListCreateAPIView):
    serializer_class = BrandSerializer

    def get_queryset(self):
        queryset = Brand.objects.annotate(min_models=Min('nr_models')).order_by('min_models')
        return queryset



@api_view(['GET'])
def show_average_pieces(request):
    if request.method == 'GET':
        red_carpet_pres_pieces_date = (
            ShowEvent.objects.values('presentation__id')
                            .annotate(average_number_of_pieces=Avg('pieces'))
                            .order_by('-average_number_of_pieces')
        )

        presentation_info = ""
        for presentation in red_carpet_pres_pieces_date:
            presentation_info += f"RedCarpetPresentation ID: {presentation['presentation__id']}, Average Pieces: {presentation['average_number_of_pieces']}                                        "


        return Response(presentation_info)


@api_view(['GET'])
def drs(request, id):
    try:
        dress = Dress.objects.get(pk=id)
    except Dress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DressSerializer2(dress)
        return Response(serializer.data)


class ReportGuests(generics.ListCreateAPIView):
    serializer_class = DressSerializer

    def get_queryset(self):
        queryset = Dress.objects.annotate(max_nr_guests=Max('showevent__presentation__nr_guests')).order_by('max_nr_guests')
        return queryset


class PresentationForDress(generics.ListCreateAPIView):
    serializer_class = ShowSerializerList

    def get_queryset(self):
        pk = self.kwargs['pk']
        query = ShowEvent.objects.filter(dress_id=pk)
        #lista = []
        #for q in query:

        return query


class DressForPresentation(generics.ListCreateAPIView):
    serializer_class = ShowSerializerList

    def get_queryset(self):
        pk = self.kwargs['pk']
        query = ShowEvent.objects.filter(presentation_id=pk)
        return query


#extra
class DressBrandView(APIView):
    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist :
            raise Http404

    def get_dress(self, pk):
        try:
            return Dress.objects.get(pk=pk)
        except Dress.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        brand = self.get_object(pk)
        dress_ids = request.data['list_of_ids']
        dresses = []
        for i in range(len(dress_ids)):
            dress = self.get_dress(dress_ids[i])
            print(dress.brand_id)
            dress.brand_id = brand
            dress.save()
            dresses.append(dress)

        serializer = BrandDressSerializer(dresses[0], data=model_to_dict(dresses[0]))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


