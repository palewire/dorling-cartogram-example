import calculate
from django.conf import settings
from django.utils import simplejson
from us_states.models import State
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Bake out data for a cartogram'
    
    def handle(self, *args, **options):
        if args[0] == '2010':
            obj_list = State.objects.filter(is_state=True).exclude(name__in=['Alaska', 'Hawaii'])
        elif args[0] == '1910':
            obj_list = State.objects.filter(is_state=True).exclude(name__in=['Alaska', 'Hawaii'])
            p = self.get_population_dict()
            for obj in obj_list:
                obj.population = int(p[obj.name])
        # Now make the cartogram
        cartogram = calculate.dorling_cartogram(
            obj_list,
            'population',
            'polygon_900913', 
            iterations=500
        )
        cartogram.make()
        data = [{
            'name': i.name,
            'circle': i.circle.wkt,
            'population': i.population
        } for i in cartogram.results]
        self.stdout.write(simplejson.dumps(data))
    
    def get_population_dict(self):
        """
        Load the populations using the state names as our guide.
        """
        import os
        import csv
        p = os.path.join(settings.ROOT_PATH, 'dorling', 'data', 'population.csv')
        r = csv.DictReader(open(p, 'r'))
        d = {}
        for i in r:
            d[i.get('STATE_OR_REGION')] = i.get('1910_POPULATION')
        return d


