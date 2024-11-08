from rest_framework import serializers 
from django.contrib.auth.models import User
from . models import *

class UserSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = User 
		fields = ('__all__')

class AccountSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = Account 
		fields = ['id', 'name']

class MeasureSerializer(serializers.ModelSerializer):
	# user_created = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

	class Meta:
		model = Measure
		fields = ['id', 'name']

	def create(self, validated_data):
		return Measure.objects.create(**validated_data)
	
	def update(self, instance, validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.save()
		return instance