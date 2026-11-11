# -*- coding: utf-8 -*-

from tornado.testing import gen_test

from tests.base import TestCase
from tests.fixtures.transformer_test_data import TestData
from thumbor.transformer import Transformer


class MinimumDimensionsTestCase(TestCase):
    @gen_test
    async def test_extreme_aspect_ratios_keep_every_dimension_at_least_one_pixel(
        self,
    ):
        cases = [
            TestData(
                source_width=16,
                source_height=16,
                target_width=800,
                target_height=20,
                halign="middle",
                valign="middle",
                focal_points=[],
                crop_left=None,
                crop_top=None,
                crop_right=None,
                crop_bottom=None,
            ),
            TestData(
                source_width=940,
                source_height=2,
                target_width=1,
                target_height=1,
                halign="middle",
                valign="middle",
                focal_points=[],
                crop_left=None,
                crop_top=None,
                crop_right=None,
                crop_bottom=None,
                fit_in=True,
            ),
            TestData(
                source_width=940,
                source_height=2,
                target_width=100,
                target_height=0,
                halign="middle",
                valign="middle",
                focal_points=[],
                crop_left=None,
                crop_top=None,
                crop_right=None,
                crop_bottom=None,
                fit_in=True,
            ),
        ]

        for case in cases:
            context = case.to_context()
            await Transformer(context).transform()

            assert context.modules.engine.calls["resize"]
            resize = context.modules.engine.calls["resize"][-1]
            assert resize["width"] >= 1
            assert resize["height"] >= 1

            for crop in context.modules.engine.calls["crop"]:
                assert crop["right"] > crop["left"]
                assert crop["bottom"] > crop["top"]
