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
"""
Custom tags

Dirk Bergstrom, krid@otisbean.com
2010-10-02

@author: krid
"""
from django import template

from journal.diary.models import INDETERMINATE_TIME

register = template.Library()

@register.simple_tag
def date_and_time(obj, field_prefix=None):
    """ Render a date or a date + time depending on what's available
    in the object.
    
    The object must be an instance of DateWithOptionalTimeMixin.
    """
    return obj.get_date_time_string(field_prefix)


@register.simple_tag
def period_dates(period):
    """ Render the possibly fuzzy dates for a period. """
    start = period.get_date_time_string('start')
    if start:
        latest_start = period.get_date_time_string('latest_start')
        if latest_start:
            start = """{0} &harr; <span class="fuzzy">{1}</span>""".\
                format(start, latest_start)
    else:
        start = INDETERMINATE_TIME

    end = period.get_date_time_string('end')
    if end:
        earliest_end = period.get_date_time_string('earliest_end')
        if earliest_end:
            end = """<span class="fuzzy">{0}</span> &harr; {1}""".\
                format(earliest_end, end)
    else:
        end = INDETERMINATE_TIME

    # FIXME Need a real arrow
    return """{0} &rArr; {1}""".format(start, end)

