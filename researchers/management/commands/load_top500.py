# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from researchers.models import Keyword, Profile
import csv

class Command(BaseCommand):

    args = '<input>'
    help = 'Call command with input file'

    def parse(self, filename):
        content = csv.reader(open(filename,'r'), delimiter=';', quotechar='"')
        result={}
        people={}
    
        for row in content:
            #Profile
            print row
            p,r=Profile.objects.get_or_create(first_name=row[1].decode('utf-8').strip(),
                                                    last_name=row[0].decode('utf-8').strip(),
                                                    unit=row[3].decode('utf-8').strip(),
                                                    email=row[6].decode('utf-8').strip())
            
            #Keywords
            keywords=row[4].split(',')
            for k in keywords:
                if k=='':
                    continue
                key = k.strip().lower()
                keyword,c = Keyword.objects.get_or_create(value=key)
                keyword.save()
                
                p.keywords.add(keyword)
                
                #People meets keywords
            p.save()

    def handle(self, *args, **options):
        import sys
        print str(sys.argv)
        self.parse(sys.argv[2])
        