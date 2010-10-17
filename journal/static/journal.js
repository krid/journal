/*
Journal
Copyright (C) 2010, Dirk Bergstrom, dirk@otisbean.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

$(document).ready(function() {
  // var original_showBubble = Timeline.OriginalEventPainter.prototype._showBubble;
  // Timeline.OriginalEventPainter.prototype._showBubble = function(x, y, evt)
  // {
  // console.log(evt);
  // return original_showBubble(x, y, evt);
  // }

  Timeline.DefaultEventSource.Event.prototype.fillInfoBubble = function(
      element, theme, labeller) {
    var url = base_url + 'details/' + this.getClassName() + '/' + this.getID() + '/'
    $.ajax( {
      url: url,
      dataType: 'html',
      success: function(data) {
        $(element).html(data)
      }
    })
  }

  // Set up the timeline
  buildTimeline();
});