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

from modules.handlers import base_emulator


class StyleHandler(base_emulator.BaseEmulator):

    def __init__(self):
        pass

    def handle(self, attack_event):
        style_path = 'modules/handlers/emulators/style/style.css'
        with open(style_path, 'r') as style_file:
            attack_event.response = style_file.read()
        return attack_event
