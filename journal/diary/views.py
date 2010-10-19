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

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest

from journal.diary.models import *
from journal.diary import models as diary_models


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
        model_types = (Activity, Entry, MedicalObservation)
    # TODO Need to honor the "private" flag on Entry (and other models?)
    for model_type in model_types:
        data['events'].extend([obj.as_timeline_dict() for obj in model_type.objects.all()])
    return HttpResponse(json.dumps(data), mimetype='application/json')


def model_details(request, model_type, pk):
    """ Render the template to fill in a bubble on the timeline. """
    try:
        # Make sure it's a type we're prepared to render.
        model_class = getattr(diary_models, model_type)
        getattr(model_class, 'as_timeline_dict')
    except AttributeError:
        return HttpResponseBadRequest("Can't render type '{0}'".format(model_type))

    obj = get_object_or_404(model_class, id=pk)
    return render_to_response('details/{0}.html'.format(model_type),
                              dict(obj=obj))
