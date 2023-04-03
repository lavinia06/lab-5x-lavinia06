from django.forms import IntegerField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Dress, Brand, RedCarpetPresentation, ShowEvent

class DressSerializer(serializers.ModelSerializer):

    max_nr_guests = serializers.IntegerField(read_only=True)
    average_models = serializers.IntegerField(read_only=True)
    def validate(self, data):
        if data['price'] < 89:
            raise ValidationError("a dress cant be under 89 euros!")
        return data


    class Meta:
        model = Dress
        fields = ['id', 'name', 'description', 'color', 'model_wearing', 'price', 'brand_id', 'max_nr_guests', 'average_models']
        #fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['nr_models'] < 0:
            raise ValidationError("the number of models must be positive!")
        return data

    class Meta:
        model = Brand
        #model.clean();
        fields = ['id', 'brand_fondator', 'brand_name', 'brand_rank', 'nr_models']


class RedCarpetSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['nr_guests'] < 0:
            raise ValidationError("the number of guests cannot be negative!")
        return data

    class Meta:
        model = RedCarpetPresentation
        fields = "__all__"
        #fields = ['id', 'holder', 'city_name']


class BrandSerializer2(serializers.ModelSerializer):
    dresses = DressSerializer(read_only=True, many = True)

    class Meta:
        model = Brand
        fields = ['id', 'brand_fondator', 'brand_name', 'brand_rank', 'nr_models', 'dresses']


class ShowSerializerList(serializers.ModelSerializer):
    class Meta:
        model = ShowEvent
        fields = ['id', 'pieces', 'show_date', 'show_popularity', 'dress', 'presentation']



class DressSerializer2(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=400)
    color = serializers.CharField(max_length=400)
    model_wearing = serializers.CharField(max_length=400)
    price = serializers.IntegerField(default=90)
    brand_id = Brand()

    class Meta:
        model = Dress
        #fields = ['id', 'name', 'description', 'color', 'model_wearing', 'price', 'brand_id', 'brand']
        fields = "__all__"
        depth = 1


class ShowEventSerializerDetail(serializers.ModelSerializer):
    id = serializers.IntegerField()
    pieces = serializers.IntegerField()
    show_date = serializers.CharField(max_length=200)
    show_popularity = serializers.IntegerField()
    dress = Dress()
    presentation = RedCarpetPresentation()

    class Meta:
        model = ShowEvent
        # fields = ['id', 'name', 'description', 'color', 'model_wearing', 'price', 'brand_id', 'brand']
        fields = "__all__"
        depth = 1

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)



class BrandDressSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Dress
        fields = ['brand_id']
