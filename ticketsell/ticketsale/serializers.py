from rest_framework import serializers
from .models import Tickets


class TicketsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tickets
        fields = ('url', 'id', 'num', 'name_start', 'name_end', 'time_start', 'time_end', 'date', 'seats',)