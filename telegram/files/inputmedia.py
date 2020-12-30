#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2020
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""Base class for Telegram InputMedia Objects."""

from typing import Union, List, Tuple

from telegram import (
    Animation,
    Audio,
    Document,
    InputFile,
    PhotoSize,
    TelegramObject,
    Video,
    MessageEntity,
)
from telegram.utils.helpers import DEFAULT_NONE, DefaultValue, parse_file_input
from telegram.utils.types import FileInput, JSONDict


class InputMedia(TelegramObject):
    """Base class for Telegram InputMedia Objects.

    See :class:`telegram.InputMediaAnimation`, :class:`telegram.InputMediaAudio`,
    :class:`telegram.InputMediaDocument`, :class:`telegram.InputMediaPhoto` and
    :class:`telegram.InputMediaVideo` for detailed use.

    """

    caption_entities: Union[List[MessageEntity], Tuple[MessageEntity, ...], None] = None

    def to_dict(self) -> JSONDict:
        data = super().to_dict()

        if self.caption_entities:
            data['caption_entities'] = [
                ce.to_dict() for ce in self.caption_entities  # pylint: disable=E1133
            ]

        return data


class InputMediaAnimation(InputMedia):
    """Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent.

    Note:
        When using a :class:`telegram.Animation` for the :attr:`media` attribute. It will take the
        width, height and duration from that video, unless otherwise specified with the optional
        arguments.

    Args:
        media (:obj:`str` | `filelike object` | :obj:`bytes` | :class:`pathlib.Path` | \
            :class:`telegram.Animation`): File to send. Pass a
            file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP
            URL for Telegram to get a file from the Internet. Lastly you can pass an existing
            :class:`telegram.Animation` object to send.

            .. versionchanged:: 13.2
               Accept :obj:`bytes` as input.
        filename (:obj:`str`, optional): Custom file name for the animation, when uploading a
            new file. Convenience parameter, useful e.g. when sending files generated by the
            :obj:`tempfile` module.

                .. versionadded:: 13.1
        thumb (`filelike object` | :obj:`bytes` | :class:`pathlib.Path`, optional): Thumbnail of
            the file sent; can be ignored if
            thumbnail generation for the file is supported server-side. The thumbnail should be
            in JPEG format and less than 200 kB in size. A thumbnail's width and height should
            not exceed 320. Ignored if the file is not uploaded using multipart/form-data.
            Thumbnails can't be reused and can be only uploaded as a new file.

            .. versionchanged:: 13.2
               Accept :obj:`bytes` as input.
        caption (:obj:`str`, optional): Caption of the animation to be sent, 0-1024 characters
            after entities parsing.
        parse_mode (:obj:`str`, optional): Send Markdown or HTML, if you want Telegram apps to show
            bold, italic, fixed-width text or inline URLs in the media caption. See the constants
            in :class:`telegram.ParseMode` for the available modes.
        caption_entities (List[:class:`telegram.MessageEntity`], optional): List of special
            entities that appear in the caption, which can be specified instead of parse_mode.
        width (:obj:`int`, optional): Animation width.
        height (:obj:`int`, optional): Animation height.
        duration (:obj:`int`, optional): Animation duration.

    Attributes:
        type (:obj:`str`): ``animation``.
        media (:obj:`str` | :class:`telegram.InputFile`): Animation to send.
        caption (:obj:`str`): Optional. Caption of the document to be sent.
        parse_mode (:obj:`str`): Optional. The parse mode to use for text formatting.
        caption_entities (List[:class:`telegram.MessageEntity`]): Optional. List of special
            entities that appear in the caption.
        thumb (:class:`telegram.InputFile`): Optional. Thumbnail of the file to send.
        width (:obj:`int`): Optional. Animation width.
        height (:obj:`int`): Optional. Animation height.
        duration (:obj:`int`): Optional. Animation duration.

    """

    def __init__(
        self,
        media: Union[FileInput, Animation],
        thumb: FileInput = None,
        caption: str = None,
        parse_mode: Union[str, DefaultValue] = DEFAULT_NONE,
        width: int = None,
        height: int = None,
        duration: int = None,
        caption_entities: Union[List[MessageEntity], Tuple[MessageEntity, ...]] = None,
        filename: str = None,
    ):
        self.type = 'animation'

        if isinstance(media, Animation):
            self.media: Union[str, InputFile] = media.file_id
            self.width = media.width
            self.height = media.height
            self.duration = media.duration
        else:
            self.media = parse_file_input(media, attach=True, filename=filename)

        if thumb:
            self.thumb = parse_file_input(thumb, attach=True)

        if caption:
            self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        if width:
            self.width = width
        if height:
            self.height = height
        if duration:
            self.duration = duration


class InputMediaPhoto(InputMedia):
    """Represents a photo to be sent.

    Args:
        media (:obj:`str` | `filelike object` | :obj:`bytes` | :class:`pathlib.Path` | \
            :class:`telegram.PhotoSize`): File to send. Pass a
            file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP
            URL for Telegram to get a file from the Internet. Lastly you can pass an existing
            :class:`telegram.PhotoSize` object to send.

            .. versionchanged:: 13.2
               Accept :obj:`bytes` as input.
        filename (:obj:`str`, optional): Custom file name for the photo, when uploading a
            new file. Convenience parameter, useful e.g. when sending files generated by the
            :obj:`tempfile` module.

                .. versionadded:: 13.1
        caption (:obj:`str`, optional ): Caption of the photo to be sent, 0-1024 characters after
            entities parsing.
        parse_mode (:obj:`str`, optional): Send Markdown or HTML, if you want Telegram apps to show
            bold, italic, fixed-width text or inline URLs in the media caption. See the constants
            in :class:`telegram.ParseMode` for the available modes.
        caption_entities (List[:class:`telegram.MessageEntity`], optional): List of special
            entities that appear in the caption, which can be specified instead of parse_mode.

    Attributes:
        type (:obj:`str`): ``photo``.
        media (:obj:`str` | :class:`telegram.InputFile`): Photo to send.
        caption (:obj:`str`): Optional. Caption of the document to be sent.
        parse_mode (:obj:`str`): Optional. The parse mode to use for text formatting.
        caption_entities (List[:class:`telegram.MessageEntity`]): Optional. List of special
            entities that appear in the caption.

    """

    def __init__(
        self,
        media: Union[FileInput, PhotoSize],
        caption: str = None,
        parse_mode: Union[str, DefaultValue] = DEFAULT_NONE,
        caption_entities: Union[List[MessageEntity], Tuple[MessageEntity, ...]] = None,
        filename: str = None,
    ):
        self.type = 'photo'
        self.media = parse_file_input(media, PhotoSize, attach=True, filename=filename)

        if caption:
            self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities


class InputMediaVideo(InputMedia):
    """Represents a video to be sent.

    Note:
        *  When using a :class:`telegram.Video` for the :attr:`media` attribute. It will take the
           width, height and duration from that video, unless otherwise specified with the optional
           arguments.
        *  ``thumb`` will be ignored for small video files, for which Telegram can easily
           generate thumb nails. However, this behaviour is undocumented and might be changed
           by Telegram.

    Args:
        media (:obj:`str` | `filelike object` | :obj:`bytes` | :class:`pathlib.Path` | \
            :class:`telegram.Video`): File to send. Pass a
            file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP
            URL for Telegram to get a file from the Internet. Lastly you can pass an existing
            :class:`telegram.Video` object to send.

            .. versionchanged:: 13.2
               Accept :obj:`bytes` as input.
        filename (:obj:`str`, optional): Custom file name for the video, when uploading a
            new file. Convenience parameter, useful e.g. when sending files generated by the
            :obj:`tempfile` module.

                .. versionadded:: 13.1
        caption (:obj:`str`, optional): Caption of the video to be sent, 0-1024 characters after
            entities parsing.
        parse_mode (:obj:`str`, optional): Send Markdown or HTML, if you want Telegram apps to show
            bold, italic, fixed-width text or inline URLs in the media caption. See the constants
            in :class:`telegram.ParseMode` for the available modes.
        caption_entities (List[:class:`telegram.MessageEntity`], optional): List of special
            entities that appear in the caption, which can be specified instead of parse_mode.
        width (:obj:`int`, optional): Video width.
        height (:obj:`int`, optional): Video height.
        duration (:obj:`int`, optional): Video duration.
        supports_streaming (:obj:`bool`, optional): Pass :obj:`True`, if the uploaded video is
            suitable for streaming.
        thumb (`filelike object` | :obj:`bytes` | :class:`pathlib.Path`, optional): Thumbnail of
            the file sent; can be ignored if
            thumbnail generation for the file is supported server-side. The thumbnail should be
            in JPEG format and less than 200 kB in size. A thumbnail's width and height should
            not exceed 320. Ignored if the file is not uploaded using multipart/form-data.
            Thumbnails can't be reused and can be only uploaded as a new file.

            .. versionchanged:: 13.2
               Accept :obj:`bytes` as input.

    Attributes:
        type (:obj:`str`): ``video``.
        media (:obj:`str` | :class:`telegram.InputFile`): Video file to send.
        caption (:obj:`str`): Optional. Caption of the document to be sent.
        parse_mode (:obj:`str`): Optional. The parse mode to use for text formatting.
        caption_entities (List[:class:`telegram.MessageEntity`]): Optional. List of special
            entities that appear in the caption.
        width (:obj:`int`): Optional. Video width.
        height (:obj:`int`): Optional. Video height.
        duration (:obj:`int`): Optional. Video duration.
        supports_streaming (:obj:`bool`): Optional. Pass :obj:`True`, if the uploaded video is
            suitable for streaming.
        thumb (:class:`telegram.InputFile`): Optional. Thumbnail of the file to send.

    """

    def __init__(
        self,
        media: Union[FileInput, Video],
        caption: str = None,
        width: int = None,
        height: int = None,
        duration: int = None,
        supports_streaming: bool = None,
        parse_mode: Union[str, DefaultValue] = DEFAULT_NONE,
        thumb: FileInput = None,
        caption_entities: Union[List[MessageEntity], Tuple[MessageEntity, ...]] = None,
        filename: str = None,
    ):
        self.type = 'video'

        if isinstance(media, Video):
            self.media: Union[str, InputFile] = media.file_id
            self.width = media.width
            self.height = media.height
            self.duration = media.duration
        else:
            self.media = parse_file_input(media, attach=True, filename=filename)

        if thumb:
            self.thumb = parse_file_input(thumb, attach=True)

        if caption:
            self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        if width:
            self.width = width
        if height:
            self.height = height
        if duration:
            self.duration = duration
        if supports_streaming:
            self.supports_streaming = supports_streaming


class InputMediaAudio(InputMedia):
    """Represents an audio file to be treated as music to be sent.

    Note:
        When using a :class:`telegram.Audio` for the :attr:`media` attribute. It will take the
        duration, performer and title from that video, unless otherwise specified with the
        optional arguments.

    Args:
        media (:obj:`str` | `filelike object` | :obj:`bytes` | :class:`pathlib.Path` | \
            :class:`telegram.Audio`):
            File to send. Pass a
            file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP
            URL for Telegram to get a file from the Internet. Lastly you can pass an existing
            :class:`telegram.Audio` object to send.

            .. versionchanged:: 13.2
               Accept :obj:`bytes` as input.
        filename (:obj:`str`, optional): Custom file name for the audio, when uploading a
            new file. Convenience parameter, useful e.g. when sending files generated by the
            :obj:`tempfile` module.

                .. versionadded:: 13.1
        caption (:obj:`str`, optional): Caption of the audio to be sent, 0-1024 characters after
            entities parsing.
        parse_mode (:obj:`str`, optional): Send Markdown or HTML, if you want Telegram apps to show
            bold, italic, fixed-width text or inline URLs in the media caption. See the constants
            in :class:`telegram.ParseMode` for the available modes.
        caption_entities (List[:class:`telegram.MessageEntity`], optional): List of special
            entities that appear in the caption, which can be specified instead of parse_mode.
        duration (:obj:`int`): Duration of the audio in seconds as defined by sender.
        performer (:obj:`str`, optional): Performer of the audio as defined by sender or by audio
            tags.
        title (:obj:`str`, optional): Title of the audio as defined by sender or by audio tags.
        thumb (`filelike object` | :obj:`bytes` | :class:`pathlib.Path`, optional): Thumbnail of
            the file sent; can be ignored if
            thumbnail generation for the file is supported server-side. The thumbnail should be
            in JPEG format and less than 200 kB in size. A thumbnail's width and height should
            not exceed 320. Ignored if the file is not uploaded using multipart/form-data.
            Thumbnails can't be reused and can be only uploaded as a new file.

            .. versionchanged:: 13.2
               Accept :obj:`bytes` as input.

    Attributes:
        type (:obj:`str`): ``audio``.
        media (:obj:`str` | :class:`telegram.InputFile`): Audio file to send.
        caption (:obj:`str`): Optional. Caption of the document to be sent.
        parse_mode (:obj:`str`): Optional. The parse mode to use for text formatting.
        caption_entities (List[:class:`telegram.MessageEntity`]): Optional. List of special
            entities that appear in the caption.
        duration (:obj:`int`): Duration of the audio in seconds.
        performer (:obj:`str`): Optional. Performer of the audio as defined by sender or by audio
            tags.
        title (:obj:`str`): Optional. Title of the audio as defined by sender or by audio tags.
        thumb (:class:`telegram.InputFile`): Optional. Thumbnail of the file to send.

    """

    def __init__(
        self,
        media: Union[FileInput, Audio],
        thumb: FileInput = None,
        caption: str = None,
        parse_mode: Union[str, DefaultValue] = DEFAULT_NONE,
        duration: int = None,
        performer: str = None,
        title: str = None,
        caption_entities: Union[List[MessageEntity], Tuple[MessageEntity, ...]] = None,
        filename: str = None,
    ):
        self.type = 'audio'

        if isinstance(media, Audio):
            self.media: Union[str, InputFile] = media.file_id
            self.duration = media.duration
            self.performer = media.performer
            self.title = media.title
        else:
            self.media = parse_file_input(media, attach=True, filename=filename)

        if thumb:
            self.thumb = parse_file_input(thumb, attach=True)

        if caption:
            self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        if duration:
            self.duration = duration
        if performer:
            self.performer = performer
        if title:
            self.title = title


class InputMediaDocument(InputMedia):
    """Represents a general file to be sent.

    Args:
        media (:obj:`str` | `filelike object` | :obj:`bytes` | :class:`pathlib.Path` | \
            :class:`telegram.Document`): File to send. Pass a
            file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP
            URL for Telegram to get a file from the Internet. Lastly you can pass an existing
            :class:`telegram.Document` object to send.

            .. versionchanged:: 13.2
               Accept :obj:`bytes` as input.
        filename (:obj:`str`, optional): Custom file name for the document, when uploading a
            new file. Convenience parameter, useful e.g. when sending files generated by the
            :obj:`tempfile` module.

                .. versionadded:: 13.1
        caption (:obj:`str`, optional): Caption of the document to be sent, 0-1024 characters after
            entities parsing.
        parse_mode (:obj:`str`, optional): Send Markdown or HTML, if you want Telegram apps to show
            bold, italic, fixed-width text or inline URLs in the media caption. See the constants
            in :class:`telegram.ParseMode` for the available modes.
        caption_entities (List[:class:`telegram.MessageEntity`], optional): List of special
            entities that appear in the caption, which can be specified instead of parse_mode.
        thumb (`filelike object` | :obj:`bytes` | :class:`pathlib.Path`, optional): Thumbnail of
            the file sent; can be ignored if
            thumbnail generation for the file is supported server-side. The thumbnail should be
            in JPEG format and less than 200 kB in size. A thumbnail's width and height should
            not exceed 320. Ignored if the file is not uploaded using multipart/form-data.
            Thumbnails can't be reused and can be only uploaded as a new file.

            .. versionchanged:: 13.2
               Accept :obj:`bytes` as input.
        disable_content_type_detection (:obj:`bool`, optional): Disables automatic server-side
            content type detection for files uploaded using multipart/form-data. Always true, if
            the document is sent as part of an album.

    Attributes:
        type (:obj:`str`): ``document``.
        media (:obj:`str` | :class:`telegram.InputFile`): File to send.
        caption (:obj:`str`): Optional. Caption of the document to be sent.
        parse_mode (:obj:`str`): Optional. The parse mode to use for text formatting.
        caption_entities (List[:class:`telegram.MessageEntity`]): Optional. List of special
            entities that appear in the caption.
        thumb (:class:`telegram.InputFile`): Optional. Thumbnail of the file to send.
        disable_content_type_detection (:obj:`bool`): Optional. Disables automatic server-side
            content type detection for files uploaded using multipart/form-data. Always true, if
            the document is sent as part of an album.

    """

    def __init__(
        self,
        media: Union[FileInput, Document],
        thumb: FileInput = None,
        caption: str = None,
        parse_mode: Union[str, DefaultValue] = DEFAULT_NONE,
        disable_content_type_detection: bool = None,
        caption_entities: Union[List[MessageEntity], Tuple[MessageEntity, ...]] = None,
        filename: str = None,
    ):
        self.type = 'document'
        self.media = parse_file_input(media, Document, attach=True, filename=filename)

        if thumb:
            self.thumb = parse_file_input(thumb, attach=True)

        if caption:
            self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        self.disable_content_type_detection = disable_content_type_detection
