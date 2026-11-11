# -*- coding: utf-8 -*-

from io import BytesIO
from os.path import dirname, join

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine


def test_resized_palette_gif_preserves_transparency():
    context = Context(
        config=Config(
            SECURITY_KEY="ACME-SEC",
            ENGINE="thumbor.engines.pil",
            PILLOW_PRESERVE_INDEXED_MODE=True,
        )
    )
    engine = Engine(context)
    sticker_path = join(
        dirname(__file__), "../course/images/sticker.gif"
    )
    with open(sticker_path, "rb") as image_file:
        engine.load(image_file.read(), ".gif")

    engine.resize(240, 160)
    image = Image.open(BytesIO(engine.read(".gif")))

    assert image.format == "GIF"
    assert "transparency" in image.info
    assert any(
        alpha == 0
        for alpha in image.convert("RGBA").getchannel("A").getdata()
    )
