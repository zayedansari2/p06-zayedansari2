# -*- coding: utf-8 -*-

from io import BytesIO

from PIL import Image
from tornado.testing import gen_test

from tests.base import FilterTestCase


class RoundCornerEdgeColorsTestCase(FilterTestCase):
    @gen_test
    async def test_transparent_round_corners_keep_edge_colors(self):
        fltr = self.get_filter(
            "thumbor.filters.round_corner", "round_corner(60,255,255,255,1)"
        )
        gray = (100, 100, 100)
        buffer = BytesIO()
        Image.new("RGBA", (200, 150), gray + (255,)).save(buffer, "PNG")
        fltr.engine.load(buffer.getvalue(), ".png")
        fltr.context.transformer.img_operation_worker()
        await fltr.run()
        image = fltr.engine.image.convert("RGBA")

        partial = 0
        darkened = 0
        for red, green, blue, alpha in image.getdata():
            if alpha == 0:
                continue
            if alpha < 255:
                partial += 1
            if any(abs(color - gray_value) > 2 for color, gray_value in zip(
                (red, green, blue), gray
            )):
                darkened += 1

        assert darkened == 0, f"{darkened} corner pixels changed color"
        assert partial > 0, "no corner pixel is partly transparent"
