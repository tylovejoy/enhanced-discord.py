"""
The MIT License (MIT)

Copyright (c) 2021-present iDevision

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Union

from .enums import ScheduledEventStatus, ScheduledEventEntityType, StagePrivacyLevel, try_enum
from .utils import parse_time
from .mixins import Hashable

if TYPE_CHECKING:
    from .state import ConnectionState
    from .guild import Guild, VocalGuildChannel
    from .types.scheduled_events import ScheduledEvent as ScheduledEventPayload


SE = TypeVar("SE", bound="ScheduledEvent")


class ScheduledEvent(Hashable):
    def __init__(self, state: ConnectionState, data: ScheduledEventPayload) -> None:
        self._state = state
        self.id = int(data["id"])

        self._update(data)

    @classmethod
    def _copy(cls: Type[SE], scheduled_event: ScheduledEvent) -> SE:
        self: SE = cls.__new__(cls)

        self.name = scheduled_event.name
        self._guild_id = scheduled_event._guild_id
        self.end_time = scheduled_event.end_time
        self.start_time = scheduled_event.start_time
        self.status = scheduled_event.status
        self.privacy_level = scheduled_event.privacy_level
        self.location_type = scheduled_event.location_type
        self._entity_id = scheduled_event._entity_id
        self._location = scheduled_event._location

    def _update(self, data: ScheduledEventPayload):
        self.name = data["name"]
        self._guild_id = data["guild_id"]

        self.end_time = parse_time(data["scheduled_end_time"])
        self.start_time = parse_time(data["scheduled_start_time"])

        self.status = try_enum(ScheduledEventStatus, data["status"])
        self.privacy_level = try_enum(StagePrivacyLevel, data["privacy_level"])
        self.location_type = try_enum(ScheduledEventEntityType, data["entity_type"])

        self._entity_id = data.get("entity_id")
        if self.location_type == ScheduledEventEntityType.location:
            self._location = data["entity_metadata"].get("location")
        else:
            self._location = None

    @property
    def guild(self) -> Optional[Guild]:
        return self._state._get_guild(int(self._guild_id))

    @property
    def location(self) -> Optional[Union[str, VocalGuildChannel]]:
        """Optional[Union[:class:`str`, :class:`VoiceChannel`, :class:`StageChannel`]
        The location of the Scheduled Event, depends on :attr:`location_type`.
        """
        if self.location_type == ScheduledEventEntityType.location:
            return self._location

        if self._entity_id is not None:
            return self._state.get_channel(int(self._entity_id))  # type: ignore
