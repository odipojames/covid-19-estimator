from rest_framework import serializers
from .models import RegionData, Region, Log
from rest_framework.validators import ValidationError


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        exclude = ("id",)


class RegionDataSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=False)

    class Meta:
        model = RegionData
        exclude = ("id",)

    def create(self, validated_data):
        reg_data = validated_data.pop("region", None)
        region = Region.objects.create(**reg_data)
        region_data = RegionData.objects.create(region=region, **validated_data)
        return region_data


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        exclude = ("id",)
