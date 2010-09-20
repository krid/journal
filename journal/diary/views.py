# Journal
# Copyright (C) 2010, Dirk Bergstrom, dirk@otisbean.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponse

from journal.diary.models import *

def timeline(request, line_type):
    params = dict(line_type=line_type,
                  today=datetime.datetime.now().strftime('%Y-%m-%d'))
    return render_to_response('timeline.html', params)

def timeline_json(request, line_type):
    data = {
            'wiki-url':"",
            'wiki-section':"",
            'dateTimeFormat': 'iso8601',
            'events': [],
            }
    if line_type == 'life':
        model_types = (Event, Period, Person)
    else: # line_type == 'diary'
        model_types = (Activity, Entry)
    # TODO Need to honor the "private" flag on Entry (and other models?)
    for model_type in model_types:
        data['events'].extend([obj.as_timeline_dict() for obj in model_type.objects.all()])
    return HttpResponse(json.dumps(data), mimetype='application/json')

def static_url(request):
    """ This is never called, it's just here so we can say {% url static %}
    in a template. """
    pass
