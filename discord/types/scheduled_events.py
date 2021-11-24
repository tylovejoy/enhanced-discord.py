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

from typing import List, Literal, Optional, TypedDict

from .user import User
from .channel import PrivacyLevel
from .snowflake import Snowflake, SnowflakeList


class ScheduledEventMetaData(TypedDict, total=False):
    location: str


class _ScheduledEventOptional(TypedDict, total=False):
    channel_id: Snowflake
    description: str
    image: str
    creator: User
    user_count: int


ScheduledEventEntityType = Literal[1, 2, 3]
ScheduledEventStatus = Literal[1, 2, 3, 4]


class ScheduledEvent(_ScheduledEventOptional):
    id: Snowflake
    guild_id: Snowflake
    creator_id: Optional[int]
    name: str
    scheduled_start_time: str
    scheduled_end_time: Optional[str]
    privacy_level: PrivacyLevel
    status: ScheduledEventStatus
    entity_type: ScheduledEventEntityType
    entity_id: Optional[Snowflake]
    entity_metadata: Optional[ScheduledEventMetaData]
