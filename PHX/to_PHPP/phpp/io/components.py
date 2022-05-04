# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Components worksheet."""

from __future__ import annotations
from typing import List, Optional

from PHX.to_PHPP.phpp import xl_app
from PHX.to_PHPP.phpp.model import component_frame, component_glazing


class Glazings:
    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self) -> int:
        xl_data = self.xl.get_single_column_data(self.sheet_name, 'ID', 1, 100,)

        for i,  val in enumerate(xl_data):
            if 'Glazing' == val:
                return i
        else:
            raise Exception(
                "Error: Cannot find the 'Glazing' header on the 'Components' sheet, column ID?")

    def find_section_first_entry_row(self) -> int:
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            self.sheet_name, 'ID', self.section_header_row, self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            if val == '01ud':
                return i
        else:
            raise Exception(
                "Error: Cannot find the 'Glazing' entry start on the 'Components' sheet, column ID?")

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()


class Frames:
    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self) -> int:
        xl_data = self.xl.get_single_column_data(self.sheet_name, 'IK', 1, 100,)

        for i,  val in enumerate(xl_data):
            if 'Window frames' == val:
                return i
        else:
            raise Exception(
                "Error: Cannot find the 'Window frames' header on the 'Components' sheet, column IK?")

    def find_section_first_entry_row(self) -> int:
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            self.sheet_name, 'IK', self.section_header_row, self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            if val == '01ud':
                return i
        else:
            raise Exception(
                "Error: Cannot find the 'Window frames' entry start on the 'Components' sheet, column IK?")

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()


class Components:
    """The PHPP Components worksheet.

    Arguments:
    ----------
        * xl (xl_app.XLConnection): The Excel Connection to use.
    """

    sheet_name = 'Components'

    def __init__(self, _xl: xl_app.XLConnection):
        self.xl = _xl
        self.glazings = Glazings(self.xl, self.sheet_name)
        self.frames = Frames(self.xl, self.sheet_name)

    def write_glazings(self, _glazing_rows: List[component_glazing.GlazingRow]) -> None:
        if not self.glazings.section_first_entry_row:
            self.glazings.section_first_entry_row = self.glazings.find_section_first_entry_row()

        for i, glazing_row in enumerate(_glazing_rows, start=self.glazings.section_first_entry_row):
            for item in glazing_row.create_xl_items(self.sheet_name, _row_num=i):
                self.xl.write_xl_item(item)

    def write_frames(self, _frame_row: List[component_frame.FrameRow]) -> None:
        if not self.frames.section_first_entry_row:
            self.frames.section_first_entry_row = self.frames.find_section_first_entry_row()

        for i, frame_row in enumerate(_frame_row, start=self.frames.section_first_entry_row):
            for item in frame_row.create_xl_items(self.sheet_name, _row_num=i):
                self.xl.write_xl_item(item)
