import calculate
import simplejson
from us_states.models import State
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Bake out data for a cartogram'
    
    def handle(self, *args, **options):
        obj_list = State.objects.filter(is_state=True).exclude(name__in=['Alaska', 'Hawaii'])
        cartogram = calculate.dorling_cartogram(
            obj_list,
            'population',
            'polygon_4326', 
            iterations=1
        )
        cartogram.make()
        data = [{
            'name': i.name,
            'circle': i.circle.wkt,
            'radius': i.radius,
            'center': i.polygon_4326.centroid.wkt
        } for i in cartogram.results]
        self.stdout.write(simplejson.dumps(data))


