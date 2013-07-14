# Copyright (C) 2012  Lukas Rist
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import re
from textwrap import dedent

import glastopf.modules.classification.sql as sql
import glastopf.modules.classification.sql_utils.responses as sql_responses
from glastopf.modules.handlers import base_emulator


class SQLiEmulator(base_emulator.BaseEmulator):
    """Emulates a SQL injection vulnerability and a successful attack."""

    def __init__(self, data_dir):
        self.sqli_c = sql.SQLiClassifier()
        self.sql_response = sql_responses.SQLResponses()
        super(SQLiEmulator, self).__init__(data_dir)

    def handle(self, attack_event):
        payload = ""
        for value_list in attack_event.http_request.request_query.values():
            value = value_list[0]
            ret = self.sqli_c.classify(value)
            if len(ret["tokens"]) > 0:
                best_query, best_ratio = self.sqli_c.query_similarity(ret["tokens"], value.lower())
                payload = self.sqli_c.token_map[best_query]
        if payload["resp"]:
            attack_event.http_request.set_raw_response(payload["resp"])
        else:
            response = self.sql_response.get_response("mysql_error").content
            payload_response = re.sub("PAYLOAD", value, response)
            attack_event.http_request.set_raw_response(dedent(payload_response))


if __name__ == "__main__":
    import glastopf.modules.events.attack as attack
    from glastopf.modules.HTTP.handler import HTTPHandler
    event = attack.AttackEvent()
    event.http_request = HTTPHandler('GET /test.php?q=SELECT%20database()', None)
    se = SQLiEmulator("/")
    se.handle(event)
    print event.http_request.get_response()